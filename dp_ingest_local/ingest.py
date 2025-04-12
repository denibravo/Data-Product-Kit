from .utils.opensearch import connect as connect_opensearch
from .utils.sql import connect as connect_sql
from .utils.ingest_comment import insert_comment
from .utils.ingest_docket import insert_docket
from .utils.ingest_document import insert_document
from .utils.ingest_opensearch import ingest_comment_from_text as insert_comment_os
from .utils.ingest_opensearch import ingest_extracted_text_from_text as insert_extracted_text_os
from .utils.ingest_summary import insert_summary


def ingest_comment(contents):
    os = connect_opensearch()
   #sql = connect_sql()
   #insert_comment(sql,contents)
    insert_comment_os(os,contents)
   #sql.commit()
   #sql.close()

def ingest_extracted_text(contents):
    os = connect_opensearch()
    insert_extracted_text_os(os,contents)


def ingest_document(contents):
    sql = connect_sql()
    insert_document(sql, contents)
    sql.commit()
    sql.close()

def ingest_docket(contents):
    sql = connect_sql()
    insert_docket(sql, contents)
    sql.commit()
    sql.close()

def ingest_summary(contents):
    sql = connect_sql()
    insert_summary(sql, contents)
    sql.commit()
    sql.close()

