## alembic升级数据库

> 1. 初始化
>   `alembic init migrations`
>
> 2. 修改alembic.ini文件中的sqlalchemy.url
>
> 3. 修改env.py文件中的target_metadata
>
>    ```python
>    import sys
>    import os
>    
>    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
>    from datacenter.models import db_meta
>    target_metadata = db_meta
>    ```
>
> 4. 创建版本
>
>    `alembic revision --autogenerate -m "message"`
>
> 5. 变更数据库
>
>    `alembic upgrade head`
