import json
from typing import Iterable, Any
from loguru import logger
import scrapy
from scrapy import cmdline
from myntra.items import MyntraItem


class PlPageSpider(scrapy.Spider):
    name = "pdp_links"
    allowed_domains = ["www.myntra.com"]

    def start_requests(self):
        cookies = {
            '_d_id': '0a039ed9-c93d-4316-87cc-5227cf36b441',
            'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTm1VMFpUazJOamt0TlRFNVlpMHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZek9UQTRORFlzSW1semN5STZJa2xFUlVFaWZRLkprRHdqN0lWQmxHRkcxY05ybkhCX25BelFLMjBqa2YyNHFZb2p2MURwYU0=',
            'mynt-eupv': '1',
            '_gcl_au': '1.1.1443091708.1750838847',
            'x-mynt-pca': 'dMfMXwZKNndyCg-wRllPxqDqrfnbwd95e5y77JwtSIdlyq-_AfqJznJdsG5JdAANYf1nEp4kY6iMPM2boBREdopvooDWzX28DIf2yWYa-5aUBhRbvilZE08_v-C4CZwNQMwnR45UAPop62k4F6wE3c5sZcFkI1oI2a8qQ_Oisj6GWYeX6WO_SA%3D%3D',
            '_scid': 'OG_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPWA',
            '_fbp': 'fb.1.1750838847780.512220360261025021',
            'tvc_VID': '1',
            '_cs_ex': '1',
            '_cs_c': '1',
            '_ScCbts': '%5B%5D',
            '_sctr': '1%7C1750789800000',
            'mynt-ulc-api': 'pincode%3A380001',
            '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled',
            '_pv': 'default',
            'dp': 'd',
            'lt_timeout': '1',
            'lt_session': '1',
            'bm_ss': 'ab8e18ef4e',
            'microsessid': '64',
            '_xsrf': 'cD1EqFwOYHU0CPGuc3ijVX634sELCWnL',
            '_ma_session': '%7B%22id%22%3A%225426b4ba-97af-4973-b965-ba41b8188366-0a039ed9-c93d-4316-87cc-5227cf36b441%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D',
            'mynt-loc-src': 'expiry%3A1750918411095%7Csource%3AIP',
            'ak_bmsc': 'A2F32B1845B5FDBEF5DC96F864074F94~000000000000000000000000000000~YAAQdA7EF5187aSXAQAAcbrIqhya4A6S8nxqXsNpjmx/cR84wdSRv/YZYDE/1EkE3Ih2N+RTueVLk7hfn0+CDgxHp0YqyZFB9eoAv7woLqV92uU4Z3STYg5FMCUtqV5uGEo0Py83HTbFmxXk8ba2I9GQsVT5wpfznHNMxVJDk9ZOzaZbtYcYsALTI0XlmsRI3tDafDV86BHSGwTNRXMdauJK3pW2Th918Tn5hx1bLbdn1uVKdj68abPhUb6nkysVymlFyxFu1UUCUzALBVG9PPMA12F1KBPFkPoEYkmNj49+cuyP2eN66h7Txbpffg38mRWc1TvdZKXvuTIGhgcwpqldyqre0WiJxKY5t7mLfsB77H3CqR+YMcaPPATfgQZdIYlUIHQJhwmgX4dF8xI3LZA/Qs291/ZyEyARYHC2JO+X8nVwBf67kE2Sh0HbgSlkszIUl36+Cc7D62/t',
            '_abck': '24639F7CCD89A18F081F73A07E70E269~0~YAAQRA7EFyfGqIyXAQAA7ujIqg460uGuGYTWWKVgtON9/Zk7iG0eA7ZuBdkkBZCXvdyc7svuRf+witD+bXtH4+ukLrRvBJPiST1TldZIHWs/nGy7hL4FEXR35rpzEIf+ejWIPAYSzkBoowDDKbXMalk73ieNCyJs2FHNbULz4CWQtmutlxkd80ze40qCi0DJ6toTwqpp4B9oaRDVjpvJJHOnQaLN4PqAAHJQpMlF+uEvOXsU5KjyLrOmAs1h1pup//jgewBd0km5QNTZOHVXkb9zXqyehlWJAWIwDvAuQN0z6o4P84IiPbU5uhT+dj4FUyAfLFhfVlQYksa5dx/yh9EGjzLwoCjGJQiw5MLEmcPvuPYQSutWum+jtWJrT6VV27f4Zl8DdIF/h0UxTp1VjDZwoHk19OWNzeyz9DmJX48c9T8Fr6Mr2pTdDyr98uEwkvJvp82HZzzEG7OSScUWFyglJfEZspbJMDp4WbXJ48Wi3/l9hPufpAtfxOUjAHp2x2GdembTLib2uHykhPZpsg/2DqqMWZdLPt2LBzp9UTV2msckQ3OpXTRNv4i4AkzECE/sJzSGQLfubcJ0ky30O4rxmIPIoIYs0n0nLLiEYsS1geWtelia3y7TQhAv~-1~-1~-1',
            'user_session': 'fuwOxZ7Mkhcte-08UImXWw.6_ozKKUTXSUg1PutRt_ruqt_1tTOVaAYxrSFOyIBzTOTk8z7qXOYnDHjaV1nBPPv4R5Swck2l2JD0I9sWzP2qGXDpqTmpsixZQBDxAox8HzGSVjRElye_VDMugDV5whvQFdtC0H5yvfmR38inrzOfg.1750916970619.86400000.hlnL73fPWCuQA3YHJSpMSIECYVko_OqxfNhkuqHe4YU',
            'bm_s': 'YAAQJg7EF5e1aaiXAQAALSbJqgM9IkJGWhfqL57/TUWfikadX0vOd/lURZ/kpLiKyJA2UlXB6QWf/4C4l9sCsckkD9rgqZdJnZ/OC4EIYFPjZa2vtZOdms9ZvBTmE/ZaKsqXgPqYs/JwJ+wqpXN9AGauJmaa8nES5PbfvnXR6G2Hep1aNjitmQHMV05tMkPN3eiNqSF/uPlXN+zO+wVVxvopFmFF3iShXIyNJUcEZG6yAPQK8D1HHl/AHOs0hXcNVUI8G1YOpW0JZaG27K5QsX045UXnGzFi/CPb/OeWwNmtAoFdz1RfLh7WsLWslZFj4oLr0zcXqllPvXnulecr57HY9gnjWkYNHvuG5KY4Os6R70GhYTlaqDwa6+FdprIZ/EwlXbJ53ptAlGzoXR1H5Zat0YJT8Uo0S30fF4E6y2v1r3kGhpIlAaaBnM2v9haPVGfheRF9S017I558X7doicH4KE14FD30UJMAf+JjmboO0VvIGlQMXm4lO61snnOsjjgOa5M+3vfViCNReuARvCTOIxLhHiHEfb9XHtVzKsBl1TcSGvBqBzVsfLzLCL1+gxmhUz6f',
            'bm_so': '7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=',
            'bm_sz': '2D91F866169FB502658FB5005B0AD486~YAAQJg7EF5q1aaiXAQAALSbJqhx0iaEYUlOGz990MvdUh2uKUzYU8BpvZHtYtD0i69Why+elCNLo2tYsRTY/gZ3nGMuhHW9eDrrGAtO2uk2IyqGpmKeGXcnVNW+BKAcnE1EpzPUan/9O1zMwmT18KNlXVeYNbLxwQQAyvD8ildu1/Z0d6pw6KW+5Fu+xSRXnTGces4NOlp8Z7wuoTm3V+8Q8UJfoPSzQjXPO7QvHyII3M6Vchd8zoLM/GPfvLTHvCrjbFKOjrvWS1FEQVfLt8QP0gkOJb53I6XkWF68t3nWC5iZ+XhbMGTO+31ekerTemommXt39ljcU5AlQKpvMarKfxktZVuqtibwzEEq2uzBlqaursXYQ7h2wcStfIhxwpNKYqDLEfFlb0Hzv5MFJbuP02fUJE/Z1nENg~3359029~4403778',
            'utm_track_v1': '%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1750916999%2C%22trackend%22%3A1750917059%7D',
            '_scid_r': 'Om_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPaQ',
            'bm_lso': '7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=^1750917001091',
            'utrid': 'XW9%2FFVdicUJTam4bakVAMCMxNDg4ODc0NzIxJDI%3D.8f11f6137cc51ca0102c67c069ce4fee',
            'bm_sv': '095E1B91BE958E52491C0A14B9FFB242~YAAQJg7EFyy3aaiXAQAAtjrJqhwZcYkLk7WwVx8sAbk8+DzjneCIGnBlNpUBYBD1B0Qe+gU5cGHJPLUu72PY/9SRG6GyIzouCibzkCyFNlMTEFIznMUescbYwpM/k4YWX+KvI+ro9sJorWpFaNymtPx0HBxRmPrqFdLfH5Qt6ozOUapjZYQ7KLdY4+CVCjIOcCBzb+c1FWEd0UNWOhSfDgiRQxxIJxQmQD7DH5vZ7IVPVZ8CVYch0FXMrWOpM02AaA==~1',
            'ak_RT': '"z=1&dm=myntra.com&si=c3903ef9-b23d-431c-a0b4-2c150e2270c5&ss=mccyr7x4&sl=3&tt=1q6&obo=2&rl=1&ld=11uu&r=48oj4cny&ul=11uw"',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-none-match': 'W/"e7841-fYh4Hp3oIOGi1arOiXKlsowF3/4"',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            # 'cookie': '_d_id=0a039ed9-c93d-4316-87cc-5227cf36b441; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTm1VMFpUazJOamt0TlRFNVlpMHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZek9UQTRORFlzSW1semN5STZJa2xFUlVFaWZRLkprRHdqN0lWQmxHRkcxY05ybkhCX25BelFLMjBqa2YyNHFZb2p2MURwYU0=; mynt-eupv=1; _gcl_au=1.1.1443091708.1750838847; x-mynt-pca=dMfMXwZKNndyCg-wRllPxqDqrfnbwd95e5y77JwtSIdlyq-_AfqJznJdsG5JdAANYf1nEp4kY6iMPM2boBREdopvooDWzX28DIf2yWYa-5aUBhRbvilZE08_v-C4CZwNQMwnR45UAPop62k4F6wE3c5sZcFkI1oI2a8qQ_Oisj6GWYeX6WO_SA%3D%3D; _scid=OG_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPWA; _fbp=fb.1.1750838847780.512220360261025021; tvc_VID=1; _cs_ex=1; _cs_c=1; _ScCbts=%5B%5D; _sctr=1%7C1750789800000; mynt-ulc-api=pincode%3A380001; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; _pv=default; dp=d; lt_timeout=1; lt_session=1; bm_ss=ab8e18ef4e; microsessid=64; _xsrf=cD1EqFwOYHU0CPGuc3ijVX634sELCWnL; _ma_session=%7B%22id%22%3A%225426b4ba-97af-4973-b965-ba41b8188366-0a039ed9-c93d-4316-87cc-5227cf36b441%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; mynt-loc-src=expiry%3A1750918411095%7Csource%3AIP; ak_bmsc=A2F32B1845B5FDBEF5DC96F864074F94~000000000000000000000000000000~YAAQdA7EF5187aSXAQAAcbrIqhya4A6S8nxqXsNpjmx/cR84wdSRv/YZYDE/1EkE3Ih2N+RTueVLk7hfn0+CDgxHp0YqyZFB9eoAv7woLqV92uU4Z3STYg5FMCUtqV5uGEo0Py83HTbFmxXk8ba2I9GQsVT5wpfznHNMxVJDk9ZOzaZbtYcYsALTI0XlmsRI3tDafDV86BHSGwTNRXMdauJK3pW2Th918Tn5hx1bLbdn1uVKdj68abPhUb6nkysVymlFyxFu1UUCUzALBVG9PPMA12F1KBPFkPoEYkmNj49+cuyP2eN66h7Txbpffg38mRWc1TvdZKXvuTIGhgcwpqldyqre0WiJxKY5t7mLfsB77H3CqR+YMcaPPATfgQZdIYlUIHQJhwmgX4dF8xI3LZA/Qs291/ZyEyARYHC2JO+X8nVwBf67kE2Sh0HbgSlkszIUl36+Cc7D62/t; _abck=24639F7CCD89A18F081F73A07E70E269~0~YAAQRA7EFyfGqIyXAQAA7ujIqg460uGuGYTWWKVgtON9/Zk7iG0eA7ZuBdkkBZCXvdyc7svuRf+witD+bXtH4+ukLrRvBJPiST1TldZIHWs/nGy7hL4FEXR35rpzEIf+ejWIPAYSzkBoowDDKbXMalk73ieNCyJs2FHNbULz4CWQtmutlxkd80ze40qCi0DJ6toTwqpp4B9oaRDVjpvJJHOnQaLN4PqAAHJQpMlF+uEvOXsU5KjyLrOmAs1h1pup//jgewBd0km5QNTZOHVXkb9zXqyehlWJAWIwDvAuQN0z6o4P84IiPbU5uhT+dj4FUyAfLFhfVlQYksa5dx/yh9EGjzLwoCjGJQiw5MLEmcPvuPYQSutWum+jtWJrT6VV27f4Zl8DdIF/h0UxTp1VjDZwoHk19OWNzeyz9DmJX48c9T8Fr6Mr2pTdDyr98uEwkvJvp82HZzzEG7OSScUWFyglJfEZspbJMDp4WbXJ48Wi3/l9hPufpAtfxOUjAHp2x2GdembTLib2uHykhPZpsg/2DqqMWZdLPt2LBzp9UTV2msckQ3OpXTRNv4i4AkzECE/sJzSGQLfubcJ0ky30O4rxmIPIoIYs0n0nLLiEYsS1geWtelia3y7TQhAv~-1~-1~-1; user_session=fuwOxZ7Mkhcte-08UImXWw.6_ozKKUTXSUg1PutRt_ruqt_1tTOVaAYxrSFOyIBzTOTk8z7qXOYnDHjaV1nBPPv4R5Swck2l2JD0I9sWzP2qGXDpqTmpsixZQBDxAox8HzGSVjRElye_VDMugDV5whvQFdtC0H5yvfmR38inrzOfg.1750916970619.86400000.hlnL73fPWCuQA3YHJSpMSIECYVko_OqxfNhkuqHe4YU; bm_s=YAAQJg7EF5e1aaiXAQAALSbJqgM9IkJGWhfqL57/TUWfikadX0vOd/lURZ/kpLiKyJA2UlXB6QWf/4C4l9sCsckkD9rgqZdJnZ/OC4EIYFPjZa2vtZOdms9ZvBTmE/ZaKsqXgPqYs/JwJ+wqpXN9AGauJmaa8nES5PbfvnXR6G2Hep1aNjitmQHMV05tMkPN3eiNqSF/uPlXN+zO+wVVxvopFmFF3iShXIyNJUcEZG6yAPQK8D1HHl/AHOs0hXcNVUI8G1YOpW0JZaG27K5QsX045UXnGzFi/CPb/OeWwNmtAoFdz1RfLh7WsLWslZFj4oLr0zcXqllPvXnulecr57HY9gnjWkYNHvuG5KY4Os6R70GhYTlaqDwa6+FdprIZ/EwlXbJ53ptAlGzoXR1H5Zat0YJT8Uo0S30fF4E6y2v1r3kGhpIlAaaBnM2v9haPVGfheRF9S017I558X7doicH4KE14FD30UJMAf+JjmboO0VvIGlQMXm4lO61snnOsjjgOa5M+3vfViCNReuARvCTOIxLhHiHEfb9XHtVzKsBl1TcSGvBqBzVsfLzLCL1+gxmhUz6f; bm_so=7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=; bm_sz=2D91F866169FB502658FB5005B0AD486~YAAQJg7EF5q1aaiXAQAALSbJqhx0iaEYUlOGz990MvdUh2uKUzYU8BpvZHtYtD0i69Why+elCNLo2tYsRTY/gZ3nGMuhHW9eDrrGAtO2uk2IyqGpmKeGXcnVNW+BKAcnE1EpzPUan/9O1zMwmT18KNlXVeYNbLxwQQAyvD8ildu1/Z0d6pw6KW+5Fu+xSRXnTGces4NOlp8Z7wuoTm3V+8Q8UJfoPSzQjXPO7QvHyII3M6Vchd8zoLM/GPfvLTHvCrjbFKOjrvWS1FEQVfLt8QP0gkOJb53I6XkWF68t3nWC5iZ+XhbMGTO+31ekerTemommXt39ljcU5AlQKpvMarKfxktZVuqtibwzEEq2uzBlqaursXYQ7h2wcStfIhxwpNKYqDLEfFlb0Hzv5MFJbuP02fUJE/Z1nENg~3359029~4403778; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1750916999%2C%22trackend%22%3A1750917059%7D; _scid_r=Om_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPaQ; bm_lso=7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=^1750917001091; utrid=XW9%2FFVdicUJTam4bakVAMCMxNDg4ODc0NzIxJDI%3D.8f11f6137cc51ca0102c67c069ce4fee; bm_sv=095E1B91BE958E52491C0A14B9FFB242~YAAQJg7EFyy3aaiXAQAAtjrJqhwZcYkLk7WwVx8sAbk8+DzjneCIGnBlNpUBYBD1B0Qe+gU5cGHJPLUu72PY/9SRG6GyIzouCibzkCyFNlMTEFIznMUescbYwpM/k4YWX+KvI+ro9sJorWpFaNymtPx0HBxRmPrqFdLfH5Qt6ozOUapjZYQ7KLdY4+CVCjIOcCBzb+c1FWEd0UNWOhSfDgiRQxxIJxQmQD7DH5vZ7IVPVZ8CVYch0FXMrWOpM02AaA==~1; ak_RT="z=1&dm=myntra.com&si=c3903ef9-b23d-431c-a0b4-2c150e2270c5&ss=mccyr7x4&sl=3&tt=1q6&obo=2&rl=1&ld=11uu&r=48oj4cny&ul=11uw"',
        }

        keyword_name = "tshirts"
        # keyword_name = "watch"

        keyword_url = f'https://www.myntra.com/{keyword_name}'
        yield scrapy.Request(url=keyword_url, cookies=cookies, headers=headers, meta={'keyword_name': keyword_name},
                             dont_filter=True)

    def parse(self, response, **kwargs):
        keyword_name = response.meta.get('keyword_name')

        json_data = response.xpath("//script[contains(text(),'searchData')]/text()").get()
        if json_data:
            json_data = json_data.replace("window.__myx =", "").strip()
            json_data = json.loads(json_data)
        else:
            json_data = json.loads(response.text)
            # logger.error("Json Data Can Not Found")

        results = json_data.get('searchData').get('results').get('products')
        if not results:
            results = results.get('products')
        if results:
            for index, result in enumerate(results):
                # Todo: Break Loop If Index Count: 25
                if index >= 25:
                    break
                index += 1

                item = MyntraItem()
                product_id = result.get('productId')
                product_url = result.get('landingPageUrl')
                if product_url:
                    product_url = f"https://www.myntra.com/{product_url}"

                # Todo: make item fileds
                item['keyword'] = keyword_name
                item['product_id'] = product_id
                item['product_url'] = product_url
                yield item

            # Todo: make requests if results(Product Counts) length < 25
            if len(results) < 25:
                next_page_url = f"https://www.myntra.com/gateway/v2/search/{keyword_name}?rows=50&o=49"
                headers = {
                    'accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
                    'app': 'web',
                    'content-type': 'application/json',
                    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNjIwNzEiLCJhcCI6IjcxODQwNzY0MyIsImlkIjoiMDM5OTk5YmZiMGNlY2I3ZiIsInRyIjoiYzJiN2VjMWZlYWVkYjdmMzgyYzdmNzI4MTYyZDIyMDMiLCJ0aSI6MTc1MDgzOTk1NjE2MSwidGsiOiI2Mjk1Mjg2In19',
                    'pagination-context': '{"scImgVideoOffset":"0_0","v":1.0,"productsRowsShown":0,"paginationCacheKey":"bc1a571d-7f0e-4a4a-ba0d-b2261a8af1be","inorganicRowsShown":0,"plaContext":"eyJwbGFPZmZzZXQiOjAsIm9yZ2FuaWNPZmZzZXQiOjMyLCJleHBsb3JlT2Zmc2V0IjowLCJmY2NQbGFPZmZzZXQiOjUwLCJzZWFyY2hQaWFub1BsYU9mZnNldCI6NDcsImluZmluaXRlU2Nyb2xsUGlhbm9QbGFPZmZzZXQiOjAsInRvc1BpYW5vUGxhT2Zmc2V0IjozLCJvcmdhbmljQ29uc3VtZWRDb3VudCI6MTQyLCJhZHNDb25zdW1lZENvdW50Ijo1MCwiZXhwbG9yZUNvbnN1bWVkQ291bnQiOjAsImN1cnNvciI6eyJTRUFSQ0giOiJmZWE6a3d0fGlkeDo0N3xzcmM6RkNDfmZlYTpua3d0fGlkeDowfHNyYzpGQ0N+ZmVhOmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQX5mZWE6bmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQSIsIlRPUF9PRl9TRUFSQ0giOiJmZWE6a3d0fGlkeDozfHNyYzpGQ0N+ZmVhOm5rd3R8aWR4OjB8c3JjOkZDQ35mZWE6a3d0fGlkeDowfHNyYzpNWU5UUkFfUExBfmZlYTpua3d0fGlkeDowfHNyYzpNWU5UUkFfUExBIn0sInBsYXNDb25zdW1lZCI6W10sImFkc0NvbnN1bWVkIjpbXSwib3JnYW5pY0NvbnN1bWVkIjpbXSwiZXhwbG9yZUNvbnN1bWVkIjpbXX0\\u003d","refresh":false,"scOffset":0,"reqId":"bc1a571d-7f0e-4a4a-ba0d-b2261a8af1be"}',
                    'priority': 'u=1, i',
                    'referer': f'https://www.myntra.com/{keyword_name}',
                    'traceparent': '00-c2b7ec1feaedb7f382c7f728162d2203-039999bfb0cecb7f-01',
                    'tracestate': '6295286@nr=0-1-3062071-718407643-039999bfb0cecb7f----1750839956161',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                    'x-meta-app': 'channel=web',
                    'x-myntra-app': 'deviceID=0a039ed9-c93d-4316-87cc-5227cf36b441;customerID=;reqChannel=web;appFamily=MyntraRetailWeb;',
                    'x-myntraweb': 'Yes',
                    'x-requested-with': 'browser',
                    'Cookie': 'mynt-loc-src=expiry%3A1750840277113%7Csource%3AIP; _d_id=0a039ed9-c93d-4316-87cc-5227cf36b441; _ma_session=%7B%22id%22%3A%2279bb0036-3955-4aad-9282-11333a95c6d0-0a039ed9-c93d-4316-87cc-5227cf36b441%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTm1VMFpUazJOamt0TlRFNVlpMHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZek9UQTRORFlzSW1semN5STZJa2xFUlVFaWZRLkprRHdqN0lWQmxHRkcxY05ybkhCX25BelFLMjBqa2YyNHFZb2p2MURwYU0=; lt_timeout=1; lt_session=1; bm_ss=ab8e18ef4e; bm_mi=B065D399E8DFEF173C366515D9C5E9DA~YAAQbw7EFxlLAXuXAQAAAqMgphxXgLwGLgMxcrrkhT6zfmR0pP8QQLCAmAKBMHiO4RnUsoxGADwfDFtxZGiBZ9YcH1tW0zSFipp9Y0x0AbfGiGWigTUbp5jw6gC/33BccZEcHcR3xIRMV2UJF/6XDPg83H1t65dGaFORvkmDwdytkram8VxHCWCyHrjPoRZDP9dR/kNVP3SLp+dJY8oPNGHNDv1AcdKU9aFZGixBAto3pmyvtwIFWwX975paN5U0kCUUGm17tYaLjzwuRC8/McYIvFv/wrAMt/+icE7zYgr0xzX3qPvYj6t9QrFy~1; microsessid=513; mynt-eupv=1; ak_bmsc=5EAA18124534C67B0A8FA77C9B670523~000000000000000000000000000000~YAAQbw7EF0lLAXuXAQAAI6cgphzZqIiijrzfMmWoj+tboSIbgRamNkfMFsDEWHhlYC+fmk4uzJXBd4FUZRPOqeyRXgKgKOSnFYwUapOCRG5ilRD2cyCzOYuuXcBbleDlxl9WKRupbV5324d06l+Lw2RC1XtDuk/TfXIS7J/rGIbVkr/2IuGxhfcHjlnG3WoMDZVwapvd1LLW06Rsz0B0cLcoPM/ujT/KdesvFChzqa7ZocQU9DqywUG835XH7KiujfIvlPLs7Tkx4wKvO7/2MoeiYVCdo5l8kdWu2Yb9WCgcIOh7iiomjrSy1xaE+6Nmen7uG+SflIeW4VBLa2VZYWqApQvy7PlxUEdYv0woS+MTRJo/Op91/NyfFQpT7wXYaetLRo+oOQZZbtBi4IaIKNULjhyuqQXFE1Jb7zDns9YFFCg9+VvAvBE8QCV0XP09h+2AO3oFg+KcWks9Ddt+yuQMSpEIVKUhN7ThTAGt; _gcl_au=1.1.1443091708.1750838847; x-mynt-pca=dMfMXwZKNndyCg-wRllPxqDqrfnbwd95e5y77JwtSIdlyq-_AfqJznJdsG5JdAANYf1nEp4kY6iMPM2boBREdopvooDWzX28DIf2yWYa-5aUBhRbvilZE08_v-C4CZwNQMwnR45UAPop62k4F6wE3c5sZcFkI1oI2a8qQ_Oisj6GWYeX6WO_SA%3D%3D; _scid=OG_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPWA; _fbp=fb.1.1750838847780.512220360261025021; tvc_VID=1; _cs_ex=1; _cs_c=1; _ScCbts=%5B%5D; _sctr=1%7C1750789800000; _abck=24639F7CCD89A18F081F73A07E70E269~0~YAAQbw7EF2NNAXuXAQAAWwEhpg6BI/9bPNWsuOZFlcumaBB5VRDvNdnQVCJpe8mLcmTXI9+P+rzup7Vx4yEEl7JTzXtkk2rVgJviCbsymtLSb8mEkahPFrbQkD9+lamN4yQBEXOJHnr1sUc53U2s2YBDmR0DD6IzC0eeol7I1PDjRg4CIjD1qWP/sPT+A/vINEwSYtD3x5uzXvkCS44g7qLSjit9jOltop8iNsP3G6f+z7yu87wsH2Zt1AjjQlHojn1dTDzwt3EgDEerR3zF/rN8ewY5rt3L8KunAEgGsKLvQtau8Kstz0rX/P2iWCVcIsLYVsPgO3lvupCSAzv5mLHCsWIi/n0JUEKCY49aAK2fGEAIdbaYOQrfYqOQ9MR9M56/h7aHZF1WHpxUauYRGO4+7HXP75LiWIxSVJ6iC7718FBhkmUJijrGFF6icNkrJ1wQMzjtDC0dibb9/o4oBTPceaKUZsV4QLKbyFOki9EZSOg8JB/gZ4Kf5MHviEPI8dlNq4OB3k2t5kNg+vFCnmoLnzYHzimanc+hP/8ppf8Mb7pUorgRBJqrx6aTYWeP/NNQJCwF3Xp+92/fsyWLyJ823W7ZIF/L9nTVsF5HOCQ58A==~-1~-1~-1; _pv=default; dp=d; _xsrf=qvHY1aQ4blb10vexGboUXbgAR21UiSfp; user_session=q-ztKQ_VuwAM0PUZ3vmpzw.1njjzW0HZGzJmejyyLxa4ZXkwe-2t3xXI645iy2FTFyuzlvtHVET_QyNdmwm3ojgv0REp2hecOP4Pc2rWe0nbOvkyT84ivVlPPiWCoTpQ1zGu8bCcUTHnth1LM3r_BI24Ps5pJUbN9TWB-0LL2yPNQ.1750839513099.86400000.jfouAHEgEci4DHZ3BhOE6Y_awAPfWLiV7q55Wy0x6xA; bm_so=AF88A2B36EDCD814A888183284B253C1C45D8F8D49C236D377365416DCF6E489~YAAQJg7EF4VLTI2XAQAAm0AxpgRnF8M4YjvgrOG2Q+eoyegYXYcsN/V18Ds0RypOr6VGhoOj56H0ZSj8pQvf8cN+2ayaHDJlloV+btUj6U0Xy0A7w+Em3KrXHLjb25LXQkWSB2KGHZVgkiAIEeLxzQ8S6MRmY32oPhyuqX8BoRo4U3XV+CJT4BPV6dbR8M12SHaZ/m7kgaBDTZy0vK54ylwxZ0he027HjCLl9BGC13swZZ3Z5r7oWQqus7wJTyRc3IcHJLO0LDLS3WwQkqtGs3Tw8P3JK5hgF2i8PJ4nNQdfcBRsgsdZ06zCc56c1drntisK85VGsBkaIJb4ZmXPudqopKr6KP0/aXS553tSYclpzVishGEi3LDqMzm2oO3EYoSmxVcQ7XogZ6V8ae4+SDaFzEtnBtKSqr5vQbqGa8qqltCvMHCI58W9VFvlVhrQm0OPeF0wTe95ik1r85Q=; bm_s=YAAQJg7EF9ZLTI2XAQAAh0UxpgNbjK5bOFJB5OWDX44GIFuLV0fSp9XCQesLV2AhSA/1UA5vY4EP6Dz7tpsg4Tf3ltskWONxsvWWaLUB25GlQC1Iyro+dvHD7itzh594N+y7fzAoa4di9ysHVZoANE8m4v/yOe83UCSomAxQQ+4MwOifpFhVTx8Pjy/SoudAohZsKFTxzrfHQvasZo5f7BORmdXLVsYJBjRoGzYkc6G6XWOmcQLUL9h4lasfyqdWbHjOmgFVysomzAc/aZ1fprQL7Tl3o4bVfLnWEjMQO4xQbzMvQTgK3My8YB2kwQtVcY4EFqC4A5C5FILIVpGA4RAig8Q5r+Wxcg6O27OB+zpn/dgiiMyGknk4W+SCs/R1cg+lml+Ir51uApWepQePS+xonboeH+EYqPTG38lGxD8wVOx+gl8+8JW8OHS4ZlWkM8YAEK883ouiIaodQWt2XYnKhdorazwhT34iS+AGN2KAunRp77LY5LB1iyIHJCQkr2XlniSq6UJbC/GU0asocV8/dfdCWdoTDMOjLGY8fYrEp54QupVrCRqovdK/i3ZZ067hDX6Q; bm_lso=AF88A2B36EDCD814A888183284B253C1C45D8F8D49C236D377365416DCF6E489~YAAQJg7EF4VLTI2XAQAAm0AxpgRnF8M4YjvgrOG2Q+eoyegYXYcsN/V18Ds0RypOr6VGhoOj56H0ZSj8pQvf8cN+2ayaHDJlloV+btUj6U0Xy0A7w+Em3KrXHLjb25LXQkWSB2KGHZVgkiAIEeLxzQ8S6MRmY32oPhyuqX8BoRo4U3XV+CJT4BPV6dbR8M12SHaZ/m7kgaBDTZy0vK54ylwxZ0he027HjCLl9BGC13swZZ3Z5r7oWQqus7wJTyRc3IcHJLO0LDLS3WwQkqtGs3Tw8P3JK5hgF2i8PJ4nNQdfcBRsgsdZ06zCc56c1drntisK85VGsBkaIJb4ZmXPudqopKr6KP0/aXS553tSYclpzVishGEi3LDqMzm2oO3EYoSmxVcQ7XogZ6V8ae4+SDaFzEtnBtKSqr5vQbqGa8qqltCvMHCI58W9VFvlVhrQm0OPeF0wTe95ik1r85Q=^1750839938265; bm_sz=464146B2940A8D0F7FF78026FA8247D0~YAAQJg7EF3FOTI2XAQAAyGwxphxv/d0T06354wwgjXQoLsnf+fEoDV6sugIl66NuuMLZucl+3v6InVjHkfc445CBGXO0ud6XIFNb198iaMZfhONE6tI1HTYGI4AK/JtKsPq9SPeTMpsdfVylBEHGsDkestn3ctrpWG8L/6JwUR4acJCPgSurKB8a4+qsY8ftrYWZ4cUB9gf+iZ6Y8x3B9Esg55ecIfDLH/AzM8HJXuXR9ILBi6bgR7+zD9PDv1WIOQp3GVsfw91w4OvW/i186uFZpsU2vlsQ5sJ8rkWbohfzTUSk9gjPEww5Q0BVBJ3JbPrD+KShlBkpjVR8aaqDqcatxLxcQtcaraztfugNK1JuPJo+HUdmUJ94AqhRhqkEh/B+UVsRQBVDISjmuvazZhY3FpPzTldCjdQ6XMemH2KLIFFLxbfKenE4KCN4NUw0iT24ofyPFuGEvF3P6gbol33vLPhze1jOUj9tnLbJ9HJYLCTZiqFzDQt4fGjug4MxvuThH40dLsRvIBJwWe2vU25G0CQVhSaYvUPekXcE7xaQSvh446gLNlhBSqey~4539952~4277573; ak_RT="z=1&dm=myntra.com&si=c3903ef9-b23d-431c-a0b4-2c150e2270c5&ss=mcbo8jdg&sl=6&tt=2h5&obo=5&rl=1"; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1750839947%2C%22trackend%22%3A1750840007%7D; utrid=G1sDfFMEZXsXUFRBAUdAMCMzMDIxMDcyMTAkMg%3D%3D.5f1520d915db4a576486c297313a464f; bm_sv=EB9722C5787D963C6D399FCBD58EE711~YAAQJg7EF8ZOTI2XAQAAnXIxphyBSvLo3rdJ/v5pddmjUp2M2A1Oq/6i49LSpu6ysDWf/kV14AiTxiT3Kp8/D7ZecZz3zn1AqofXI3N1gXAJP31xMSQjoI0ED6LxbgIJdCtSpSHmVpClkzu+WOlEfn2XgLbYjto2nxKtPyhXDVaP92XkQX2xX/P2sRgOOjxeeGQJ6ZStPGPPMO48att9CC7Dn71S3axC9uk2GYIiIuyYVYQ8iLTzhRUw19HGi0zNpw==~1; _scid_r=P2_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPbg; _abck=24639F7CCD89A18F081F73A07E70E269~-1~YAAQVA7EF2OdlqKXAQAAgxMzpg5Bydf8yjWay+wXI1s0KO5N8ol/fnxH1323EdiKkztdvBfocrsKh32zFs4Izrb3cI9VxOnL7K9Hp9F+AqklnK317xZVGJIHnAwVpuS+OuW76wM0xmFEXXzT3jZCThNNq+pExkP6uNFGa+nNmknOuh0ral5tn4f9zjd7kK6DIGh55O14PGViExGSuvDrC7PPwlJVflcxWiftdONmSDbgBY/Jx8GELQY/EQ+HgkyInDj/Ri9gSHED2pqrLMZyr8lcRQ3IFjmTSO87yl6DwFlVpTfECjfJm2fFN4cCWIXdgP8WBmC8L/xMUIwjoNPww04ioKoOwkvjwiZvnWCJJeg0oZHMdsJKGT1LNv+YXOuAGdOabLEQMmIxu0AsftXEbUbl2TEYOt0j3HiKwbD9phlRVrIbt79I6ufBP8bh4nKcg7LoHjSRHERifOjqf+an3NPgFjAqNJlZPYyeKvZpNTNikiBdHptoZA8AskZw/HEEMdabeXVpm+3isNauv7cDUyBR0VA1nFxqHKpTzt4Tq6JzCnIKTMO1uXdm/GCf8leKizTibqlpYfsT/4+wxjpnZcgbRa7lQfRXVyxbcxIB88FILA==~0~-1~-1; bm_s=YAAQNQ7EF48sS4OXAQAADNLYpQPc0fWhD1X0SpZwjGgvmjW9nefjPVBliojaA6xpEvqR4XbclhBNI52nSIPI7oawJTSTKj6s1g9d17cp/I6wkibwmlFZBflKDHVXEw/OLaI5sZZFOdzV5xRildc4hAJPZBiUu7AygMk4/RNf59xfaQpstEIpa8e/Reh9bBxCJgUENEtqzyICSZA680kkDWnUjmT0fzzu0JPyhU5geFPR5Df+ARol5n1LCA6Gx3px4aZ1owFun0kGhrvC+OkIoy214iswJXLFgP4MufKFvstcDXq2R5poPjaDFQNK/qmONIuMNUsWZsATqRriXZXz5vAHbp0EAVUsMpNFbEEfrVyIp1JXj3c6CvtRlLcArAXRmZ2GhljBhwyjoJ7XH0S3+ktcaklNHRISQQJLuEsOv7jXOUOOXS16MZPYupUhyrQucxKyfThf32nW7v+DjGvQgJm5R4nIPhwdB6Yxzz7Poqn3wquOJfRNN7ardZrh4quuvktBPhtUPqnIaKEVdjxlPgTA7ZzkHyoa3jWhgHbOLRVwXthLRucWpKjCTKNeAD57IKWGCeD8; bm_so=553845FE0C1875B56DA0D2DAEEAF529883697C27DB1831E48A59AE70C98664C0~YAAQNQ7EF5AsS4OXAQAADdLYpQSFF8EP7BdfQ5eMiumddZlv3I1ecvHuPhhBoCiJH5XCsCo+FMnfyaouAW2dnIuflQ+b+GZrDMMmctOxiKf7mjhLWauo7n7f3PC9K+2xUAk0Bw/ZZ+SaNHHPLY6nzVuMZaGaNUMYsupDJRAK6zETejYWbkF95cQ8w2GyK5W5pSyaDadlWZtuPsPQwzgpj/VGgFE1SHEtpN1DrUUp0le7+19PStpHNh6NU2MUjQSH+f0sXz+b/nkME0K7hSToDTmGOANWfHK6VROrLKBcgSyw2TWfjwRkkcAxK3Mhj234DDZMAFvMQigBjZ3p+cxx65CsaaNUpqW2NEe5MAEXV0qKHGg0YWmomE4J1YTrQyKxxDxe+GE0Q8eJOb4toywEoXRO4+yKuSL6PYdajK2nvI5k/nBJIVfgZ5RZwliMak106c/F10w/ShARfl4aYtQ=; bm_sv=EB9722C5787D963C6D399FCBD58EE711~YAAQVA7EF2SdlqKXAQAAgxMzphxOHu2CjGDw33EZXcNU9IWBvVDlRmonqhAbBzFJn2KRvp/7EtaGg3f2g7VaOLAIIDXhrlFDVBMg/mO/iRIJc1AH/46Wa1GDjdaa5SMvbBG5kDxPTw9m7S7VvdsUo/TGHWikKrNp9pybNmv8zcDG17pNqrRjV5o0liF4smgsiH+0325+TGXbTkrJJO2XQCgfrkeL5VkDGZhUpepgu7UTq5MPcM2oMZwkvh7yKXCp0Q==~1; bm_sz=A916048D2B42F17364CF157E29BAB788~YAAQdg7EFw4JDX+XAQAAC0LepRwXgw83UvU8TGgKjjlWbFw3Vh4JsYPp+KClwWx2V0Wh3k21s9TnNX89DfqPcx+R+b5G7MYIyCbFEODjFRMMMmDGzmD3VgRXECW4NLDrZSpxkhujhRNBVabIcXxdEOWQksEm+pWzhJNQgFpLAKbxIBt5SC7K1IfKMtaZegPa1pENQ+Q8AwnOwrEyZ186zc4kf8jT4rMl5bG+DH6Qyd4ji+SfFjdi8pw8w56AZoIsa+ahcWHJ0PMQUhFUiXSrXEiyeFA268p2XgOr/Eu64KN1UOyDDmKHEIdRJIteyOZMqIAFIqtflkzt6alr8OL+P2HU1vfrsn3gfPG1POVTP3d/AGQsPaLm17H1hhTVG8T5nhh1MmbY44fDVR8rKJHTP7Wp3fh2+uvXaIpP/uiTx50AX+hWjlHxzNHMMCKgGT0=~3686967~4276802; utrid=U3wOFE9kR1UUTQlZaF5AMCMyMDgyODQ1NDIxJDI%3D.f178fd9fa549c46e6e1349def7929bc9'
                }
                yield scrapy.Request(url=next_page_url, headers=headers, meta={'keyword_name': keyword_name},
                                     dont_filter=True)
        else:
            logger.error("Product Details Can Not Found")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PlPageSpider.name}".split())
