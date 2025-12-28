import requests

cookies = {
    'session-id': '257-8040309-8910054',
    'i18n-prefs': 'INR',
    'ubid-acbin': '258-5664222-5194852',
    'session-token': '3vJV6kVvkEqqIpedcJMVi9jRJ1Fo/pjJyuPVZlwABxAluhuN97ccASPNPuErCDSVFHrpA3fzMRJQ1uiz6uy7caitv80m952JSO9BxQF4vd6RAmsiUIxgllKLiay0WwaBz76Tt/xJ6xwg8V3mC3jvZ9LC9MBZDudgs0nHKbgDga3CMvxbnJV+Eg/L0nNNzOpkQ3TCgU0qx7UOZPaFh5NGeUkLIJY1fF50LJ4oTg/x7+yOx3y228pA0SvfAkNDXqTgYsozcXJVBdojBeokhlUi6msOzJ+QPEZFhoFwXmPA52oqNkpKlH51azkUK+74XkEOUXi0Q3wqsKDMtPX2Si9ElwACjwml20gR',
    'csm-hit': 'tb:FBRKC810APG8EAEH5E5N+s-8VZPMXCF67M5ZX2Y1BTK|1740125519389&t:1740125519389&adb:adblk_no',
    'session-id-time': '2082758401l',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'device-memory': '8',
    'downlink': '9.65',
    'dpr': '1.2000000000000002',
    'ect': '4g',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.amazon.in/s?k=namkeen',
    'rtt': '100',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1.2000000000000002',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '1600',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'viewport-width': '1600',
    # 'cookie': 'session-id=257-8040309-8910054; i18n-prefs=INR; ubid-acbin=258-5664222-5194852; session-token=3vJV6kVvkEqqIpedcJMVi9jRJ1Fo/pjJyuPVZlwABxAluhuN97ccASPNPuErCDSVFHrpA3fzMRJQ1uiz6uy7caitv80m952JSO9BxQF4vd6RAmsiUIxgllKLiay0WwaBz76Tt/xJ6xwg8V3mC3jvZ9LC9MBZDudgs0nHKbgDga3CMvxbnJV+Eg/L0nNNzOpkQ3TCgU0qx7UOZPaFh5NGeUkLIJY1fF50LJ4oTg/x7+yOx3y228pA0SvfAkNDXqTgYsozcXJVBdojBeokhlUi6msOzJ+QPEZFhoFwXmPA52oqNkpKlH51azkUK+74XkEOUXi0Q3wqsKDMtPX2Si9ElwACjwml20gR; csm-hit=tb:FBRKC810APG8EAEH5E5N+s-8VZPMXCF67M5ZX2Y1BTK|1740125519389&t:1740125519389&adb:adblk_no; session-id-time=2082758401l',
}

url = "https://www.amazon.in/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A66259&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_1&ds=v1%3ABY8YqeR9FSYyPETbM774iA8kfMO2GkwDJ%2BsO0FmS40o"

original_url = 'https://www.amazon.in/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A66259&dc&ds=v1%3A02%2F9L51JddriZr6qz%2Bj'
'%2FdMbyRSsT4H8m7PIqPezP30A&qid=1740124523&rnid=91049095031&ref=sr_nr_p_123_1'

response = requests.get(
    url,
    cookies=cookies,
    headers=headers,
)

print(response.status_code)