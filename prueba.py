from aiohttp import ClientSession
from os import environ

import asyncio
import csv

async def main_operation(session: ClientSession = None, repo_name: str = None, headers: dict = None, owner: str = None) -> dict:
    repo_info = {
        'repo name': repo_name,
        'link': f'https://github.com/{owner}/{repo_name}'
    }

    cp_url = f'https://api.github.com/repos/{owner}/{repo_name}/properties/values'
    async with session.get(url=cp_url, headers=headers) as response:
        if response.status == 200:
            repo_data = await response.json()
            for cp in repo_data:
                pass

    return repo_info


async def control(csv_data: list = None, repo_names: list = repo_names, headers: dict = None, owner: str = None):

    async with ClientSession() as session:
        tasks = []
        results = []
        for repo in repo_names:
            task = asyncio.create_task(main_operation(session = session, repo_name=repo, headers=headers, owner=owner))
            tasks.append(task)

        for task in tasks:
            result = await task
            if result:
                results.append(result)
        csv_data += results


if __name__ == "__main__":
    OWNER = '' # {orga name}
    repo_names = []
    headers = {
            'Authorization': f'Bearer {environ['GHPT']}'
        }
    control_tasks = []
    csv_data = []

    asyncio.run(control(csv_data=csv_data,repo_names=repo_names, headers=headers, owner=OWNER))

    with open(f'asyncinfo.csv','w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(csv_data[0].keys())
        for i in csv_data:
            csv_writer.writerow(i.values())