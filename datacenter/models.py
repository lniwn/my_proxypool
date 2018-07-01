# !/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

db_meta = sa.MetaData()
BaseTable = declarative_base(metadata=db_meta)


class ProxyTbl(BaseTable):
    __tablename__ = 'tbl_proxy'
    __table_args__ = (
        {'extend_existing': True},
    )

    host = sa.Column(sa.String(100), nullable=False, primary_key=True)
    port = sa.Column(sa.Integer, nullable=False, primary_key=True)
    scheme = sa.Column(sa.String(10), nullable=False)
    country = sa.Column(sa.String(20), nullable=True)
    area = sa.Column(sa.String(20), nullable=True)
    update_time = sa.Column(sa.TIMESTAMP(True), nullable=False,
                            server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return "<Proxy(host='%s', port=%d, scheme='%s', country='%s, area=%s, update_time=%s')>" % (
            self.host, self.port, self.scheme, self.country, self.area, self.update_time
        )
