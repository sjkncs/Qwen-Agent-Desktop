# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from typing import List, Tuple

from qwen_agent.log import logger
from qwen_agent.tools.base import register_tool
from qwen_agent.tools.doc_parser import Record
from qwen_agent.tools.search_tools.base_search import BaseSearch


def _try_move_faiss_to_gpu(index):
    """Move a CPU FAISS index to GPU if faiss-gpu is available and CUDA is present."""
    try:
        import faiss
        if not hasattr(faiss, 'StandardGpuResources'):
            return index
        res = faiss.StandardGpuResources()
        gpu_index = faiss.index_cpu_to_gpu(res, 0, index)
        logger.info('[VectorSearch] FAISS index moved to GPU (faiss-gpu).')
        return gpu_index
    except Exception as e:
        logger.debug(f'[VectorSearch] GPU FAISS not available, using CPU: {e}')
        return index


def _get_embeddings():
    """
    Return a LangChain-compatible embeddings object.
    Priority:
      1. DashScopeEmbeddings  – if DASHSCOPE_API_KEY is set
      2. HuggingFaceEmbeddings (sentence-transformers) – local, free, GPU-accelerated
    """
    dashscope_key = os.getenv('DASHSCOPE_API_KEY', '')
    if dashscope_key:
        try:
            from langchain_community.embeddings import DashScopeEmbeddings
            logger.info('[VectorSearch] Using DashScope embeddings (text-embedding-v1).')
            return DashScopeEmbeddings(model='text-embedding-v1', dashscope_api_key=dashscope_key)
        except ImportError:
            pass

    # Fallback: local sentence-transformers model (GPU-accelerated on RTX 5060 Ti)
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        try:
            import torch
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        except ImportError:
            device = 'cpu'
        model_name = os.getenv('QWEN_AGENT_EMBED_MODEL', 'BAAI/bge-m3')
        logger.info(f'[VectorSearch] Using HuggingFace embeddings: {model_name} on {device}.')
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True, 'batch_size': 64},
        )
    except ImportError:
        raise ImportError(
            'No embedding backend found. Either:\n'
            '  1. Set DASHSCOPE_API_KEY and install langchain_community, or\n'
            '  2. Install sentence-transformers: pip install sentence-transformers langchain_community'
        )


@register_tool('vector_search')
class VectorSearch(BaseSearch):

    def sort_by_scores(self, query: str, docs: List[Record], **kwargs) -> List[Tuple[str, int, float]]:
        try:
            from langchain.schema import Document
        except ModuleNotFoundError:
            raise ModuleNotFoundError('Please install langchain by: `pip install langchain`')
        try:
            from langchain_community.vectorstores import FAISS
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                'Please install langchain_community: `pip install langchain_community`, '
                'and faiss: `pip install faiss-gpu` (CUDA) or `pip install faiss-cpu`')

        # Extract raw query text from JSON if needed
        try:
            query_json = json.loads(query)
            if 'text' in query_json:
                query = query_json['text']
        except json.decoder.JSONDecodeError:
            pass

        # Flatten all chunks
        all_chunks = []
        for doc in docs:
            for chk in doc.raw:
                all_chunks.append(Document(page_content=chk.content[:2000], metadata=chk.metadata))

        if not all_chunks:
            return []

        embeddings = _get_embeddings()
        db = FAISS.from_documents(all_chunks, embeddings)

        # Attempt GPU acceleration for the FAISS index
        db.index = _try_move_faiss_to_gpu(db.index)

        chunk_and_score = db.similarity_search_with_score(query, k=len(all_chunks))
        return [(chk.metadata['source'], chk.metadata['chunk_id'], score) for chk, score in chunk_and_score]
