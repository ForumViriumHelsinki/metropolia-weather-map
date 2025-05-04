import asyncio
import os

import asyncpg

DB_NAME = os.environ.get("DB_NAME", "weatherdb")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "pass")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def run_sql_files_in_folder(connection_string, folder_path):
	"""
	Executes all SQL files in the specified folder to populate the database.

	:param connection_string: PostgreSQL connection string.
	:param folder_path: Path to the folder containing SQL files.
	"""
	try:
		sql_files = sorted(
			[f for f in os.listdir(folder_path) if f.endswith(".sql")]
		)
		print(sql_files)
		async with asyncpg.create_pool(connection_string) as pool:
			for sql_file in sql_files:
				sql_file_path = os.path.join(folder_path, sql_file)
				async with pool.acquire() as conn:
					with open(sql_file_path, "r") as file:
						sql_script = file.read()
						await conn.execute(
							sql_script
						)  # This ensures the script finishes before proceeding
					print(f"Successfully executed SQL file: {sql_file}")
	except Exception as e:
		print(f"Error executing SQL files in folder {folder_path}: {e}")


if __name__ == "__main__":
	folder_path = os.path.join(os.path.dirname(__file__))
	asyncio.run(run_sql_files_in_folder(DATABASE_URL, folder_path))
