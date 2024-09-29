class BSBIIndex(BSBIIndex):
    def retrieve(self, query):
        """Retrieves the documents corresponding to the conjunctive query
        
        Parameters
        ----------
        query: str
            Space separated list of query tokens
            
        Result
        ------
        List[str]
            Sorted list of documents which contains each of the query tokens. 
            Should be empty if no documents are found.
        
        Should NOT throw errors for terms not in corpus
        """
        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        ### Begin your code
        query_terms = query.split()
        if not query_terms:
            return []

        with InvertedIndexMapper(self.index_name, postings_encoding=self.postings_encoding, directory=self.output_dir) as mapper:
            try:
                # 获取第一个查询词的倒排列表
                result = mapper[self.term_id_map[query_terms[0]]]
                for term in query_terms[1:]:
                    result = sorted_intersect(result, mapper[self.term_id_map[term]])
            except KeyError:
                # 如果查询词不在索引中，返回空列表
                return []

        # 将文档ID转换为文档名称
        return [self.doc_id_map[doc_id] for doc_id in result]
        ### End your code
