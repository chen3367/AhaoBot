"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def insert(self, table: str, **kwargs) -> tuple:
        await self.connection.execute(
            f"INSERT INTO {table} ({', '.join(kwargs.keys())}) VALUES ({', '.join('?' * len(kwargs))})",
            tuple(kwargs.values())
        )
        await self.connection.commit()

        result = await self.select_one(table, "*", **kwargs)
        return result
        
    async def delete(self, table: str, **kwargs) -> list:
        if not kwargs:
            result = await self.select(table, "*")
            await self.connection.execute(f"DELETE FROM {table}")
        else:
            result = await self.select(table, "*", **kwargs)
            await self.connection.execute(
                f"DELETE FROM {table} WHERE {(' AND ').join(map(lambda x: f'{x}=?', kwargs.keys()))}",
                tuple(kwargs.values())
            )
        await self.connection.commit()

        return result
    
    async def select_one(self, table: str, *cols, **kwargs) -> list:
        if not kwargs:
            rows = f"SELECT {(', ').join(cols)} FROM {table}"
        else:
            rows = await self.connection.execute(
                f"SELECT {(', ').join(cols)} FROM {table} WHERE {(' AND ').join(map(lambda x: f'{x}=?', kwargs.keys()))}",
                tuple(kwargs.values())
            )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result
    
    async def select(self, table: str, *cols, **kwargs) -> list:
        if not kwargs:
            rows = f"SELECT {(', ').join(cols)} FROM {table}"
        else:
            rows = await self.connection.execute(
                f"SELECT {(', ').join(cols)} FROM {table} WHERE {(' AND ').join(map(lambda x: f'{x}=?', kwargs.keys()))}",
                tuple(kwargs.values())
            )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list