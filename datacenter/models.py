# !/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

db_meta = sa.MetaData()
BaseTable = declarative_base(metadata=db_meta)


class ProxyTbl(BaseTable):
    __tablename__ = 'tbl_proxy'
    # __table_args__ = (sa.PrimaryKeyConstraint('ip', 'port', name='ip_port'),)

    ip = sa.Column(sa.String(100), nullable=False, primary_key=True)
    port = sa.Column(sa.Integer, nullable=False, primary_key=True)
    scheme = sa.Column(sa.String(10), nullable=False)
    location = sa.Column(sa.String(50), nullable=True)

    def __repr__(self):
        return "<Proxy(ip='%s', port=%d, scheme='%s', location='%s')>" % (
            self.ip, self.port, self.scheme, self.location
        )
