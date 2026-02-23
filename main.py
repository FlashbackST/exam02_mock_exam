#!/usr/bin/env python3

import base64
import io
import select
import sys
import termios
import time
import tty
import random
import shlex
import shutil
import subprocess
import threading
from pathlib import Path

# ---------------------------------------------------------------------------
# Solutions (base64-encoded, revealed only on finish)
# ---------------------------------------------------------------------------
_SOLUTIONS = {'level1': {'first_word': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50IG1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoKCWlmIChhYyA9PSAyKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSA9PSAnICcgfHwgYXZbMV1baV0gPT0gJ1x0JykKCQkJaSsrOwoJCXdoaWxlIChhdlsxXVtpXSAmJiBhdlsxXVtpXSAhPSAnICcgJiYgYXZbMV1baV0gIT0gJ1x0JykKCQkJd3JpdGUoMSwgJmF2WzFdW2krK10sIDEpOwoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'fizzbuzz': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKdm9pZAlwdXRfbmJyKGludCBuKQp7CgljaGFyIGM7CgoJaWYgKG4gPj0gMTApCgkJcHV0X25icihuIC8gMTApOwoJYyA9ICcwJyArIG4gJSAxMDsKCXdyaXRlKDEsICZjLCAxKTsKfQoKaW50CW1haW4odm9pZCkKewoJaW50IGk7CgoJaSA9IDE7Cgl3aGlsZSAoaSA8PSAxMDApCgl7CgkJaWYgKGkgJSAxNSA9PSAwKQoJCQl3cml0ZSgxLCAiZml6emJ1enoiLCA4KTsKCQllbHNlIGlmIChpICUgMyA9PSAwKQoJCQl3cml0ZSgxLCAiZml6eiIsIDQpOwoJCWVsc2UgaWYgKGkgJSA1ID09IDApCgkJCXdyaXRlKDEsICJidXp6IiwgNCk7CgkJZWxzZQoJCQlwdXRfbmJyKGkpOwoJCXdyaXRlKDEsICJcbiIsIDEpOwoJCWkrKzsKCX0KCXJldHVybiAoMCk7Cn0K', 'ft_putstr': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKdm9pZAlmdF9wdXRzdHIoY2hhciAqc3RyKQp7CglpbnQgaTsKCglpID0gMDsKCXdoaWxlIChzdHJbaV0pCgkJd3JpdGUoMSwgJnN0cltpKytdLCAxKTsKfQo=', 'ft_strcpy': 'Y2hhcgkqZnRfc3RyY3B5KGNoYXIgKmRlc3QsIGNoYXIgKnNyYykKewoJaW50IGk7CgoJaSA9IDA7Cgl3aGlsZSAoc3JjW2ldKQoJewoJCWRlc3RbaV0gPSBzcmNbaV07CgkJaSsrOwoJfQoJZGVzdFtpXSA9ICdcMCc7CglyZXR1cm4gKGRlc3QpOwp9Cg==', 'ft_strlen': 'aW50CWZ0X3N0cmxlbihjaGFyICpzdHIpCnsKCWludCBpOwoKCWkgPSAwOwoJd2hpbGUgKHN0cltpXSkKCQlpKys7CglyZXR1cm4gKGkpOwp9Cg==', 'ft_swap': 'dm9pZAlmdF9zd2FwKGludCAqYSwgaW50ICpiKQp7CglpbnQgdG1wOwoKCXRtcCA9ICphOwoJKmEgPSAqYjsKCSpiID0gdG1wOwp9Cg==', 'repeat_alpha': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CglpbnQgcG9zOwoKCWlmIChhYyA9PSAyKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQl7CgkJCWlmICgoYXZbMV1baV0gPj0gJ2EnICYmIGF2WzFdW2ldIDw9ICd6JykKCQkJCXx8IChhdlsxXVtpXSA+PSAnQScgJiYgYXZbMV1baV0gPD0gJ1onKSkKCQkJewoJCQkJcG9zID0gKGF2WzFdW2ldIHwgMzIpIC0gJ2EnICsgMTsKCQkJCWogPSAwOwoJCQkJd2hpbGUgKGorKyA8IHBvcykKCQkJCQl3cml0ZSgxLCAmYXZbMV1baV0sIDEpOwoJCQl9CgkJCWVsc2UKCQkJCXdyaXRlKDEsICZhdlsxXVtpXSwgMSk7CgkJCWkrKzsKCQl9Cgl9Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'rev_print': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoKCWlmIChhYyA9PSAyKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQkJaSsrOwoJCXdoaWxlIChpID4gMCkKCQkJd3JpdGUoMSwgJmF2WzFdWy0taV0sIDEpOwoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'rot_13': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQljID0gYXZbMV1baV07CgkJCWlmIChjID49ICdhJyAmJiBjIDw9ICd6JykKCQkJCWMgPSAoYyAtICdhJyArIDEzKSAlIDI2ICsgJ2EnOwoJCQllbHNlIGlmIChjID49ICdBJyAmJiBjIDw9ICdaJykKCQkJCWMgPSAoYyAtICdBJyArIDEzKSAlIDI2ICsgJ0EnOwoJCQl3cml0ZSgxLCAmYywgMSk7CgkJCWkrKzsKCQl9Cgl9Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'rotone': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQljID0gYXZbMV1baV07CgkJCWlmIChjID09ICd6JykKCQkJCWMgPSAnYSc7CgkJCWVsc2UgaWYgKGMgPT0gJ1onKQoJCQkJYyA9ICdBJzsKCQkJZWxzZSBpZiAoKGMgPj0gJ2EnICYmIGMgPD0gJ3knKSB8fCAoYyA+PSAnQScgJiYgYyA8PSAnWScpKQoJCQkJYysrOwoJCQl3cml0ZSgxLCAmYywgMSk7CgkJCWkrKzsKCQl9Cgl9Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'search_and_replace': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gNCAmJiBhdlsyXVswXSAmJiAhYXZbMl1bMV0gJiYgYXZbM11bMF0gJiYgIWF2WzNdWzFdKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQl7CgkJCWMgPSBhdlsxXVtpXTsKCQkJaWYgKGMgPT0gYXZbMl1bMF0pCgkJCQljID0gYXZbM11bMF07CgkJCXdyaXRlKDEsICZjLCAxKTsKCQkJaSsrOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo=', 'ulstr': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQljID0gYXZbMV1baV07CgkJCWlmIChjID49ICdhJyAmJiBjIDw9ICd6JykKCQkJCWMgLT0gMzI7CgkJCWVsc2UgaWYgKGMgPj0gJ0EnICYmIGMgPD0gJ1onKQoJCQkJYyArPSAzMjsKCQkJd3JpdGUoMSwgJmMsIDEpOwoJCQlpKys7CgkJfQoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg=='}, 'level2': {'alpha_mirror': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQljID0gYXZbMV1baV07CgkJCWlmIChjID49ICdhJyAmJiBjIDw9ICd6JykKCQkJCWMgPSAneicgLSAoYyAtICdhJyk7CgkJCWVsc2UgaWYgKGMgPj0gJ0EnICYmIGMgPD0gJ1onKQoJCQkJYyA9ICdaJyAtIChjIC0gJ0EnKTsKCQkJd3JpdGUoMSwgJmMsIDEpOwoJCQlpKys7CgkJfQoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'camel_to_snake': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQljID0gYXZbMV1baV07CgkJCWlmIChjID49ICdBJyAmJiBjIDw9ICdaJykKCQkJewoJCQkJaWYgKGkgPiAwKQoJCQkJCXdyaXRlKDEsICJfIiwgMSk7CgkJCQljICs9IDMyOwoJCQl9CgkJCXdyaXRlKDEsICZjLCAxKTsKCQkJaSsrOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo=', 'do_op': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgojaW5jbHVkZSA8c3RkbGliLmg+Cgp2b2lkCXB1dF9uYnIoaW50IG4pCnsKCWNoYXIgYzsKCglpZiAobiA8IDApCgl7CgkJd3JpdGUoMSwgIi0iLCAxKTsKCQluID0gLW47Cgl9CglpZiAobiA+PSAxMCkKCQlwdXRfbmJyKG4gLyAxMCk7CgljID0gJzAnICsgbiAlIDEwOwoJd3JpdGUoMSwgJmMsIDEpOwp9CgppbnQJbWFpbihpbnQgYWMsIGNoYXIgKiphdikKewoJaW50CQlhOwoJaW50CQliOwoJaW50CQlyZXN1bHQ7CgljaGFyCW9wOwoKCWlmIChhYyAhPSA0KQoJewoJCXdyaXRlKDEsICJcbiIsIDEpOwoJCXJldHVybiAoMCk7Cgl9CglhID0gYXRvaShhdlsxXSk7CglvcCA9IGF2WzJdWzBdOwoJYiA9IGF0b2koYXZbM10pOwoJaWYgKG9wID09ICcrJykKCQlyZXN1bHQgPSBhICsgYjsKCWVsc2UgaWYgKG9wID09ICctJykKCQlyZXN1bHQgPSBhIC0gYjsKCWVsc2UgaWYgKG9wID09ICcqJykKCQlyZXN1bHQgPSBhICogYjsKCWVsc2UgaWYgKG9wID09ICcvJykKCQlyZXN1bHQgPSBhIC8gYjsKCWVsc2UgaWYgKG9wID09ICclJykKCQlyZXN1bHQgPSBhICUgYjsKCWVsc2UKCXsKCQl3cml0ZSgxLCAiXG4iLCAxKTsKCQlyZXR1cm4gKDApOwoJfQoJcHV0X25icihyZXN1bHQpOwoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'ft_atoi': 'aW50CWZ0X2F0b2koY29uc3QgY2hhciAqc3RyKQp7CglpbnQgaTsKCWludCBzaWduOwoJaW50IHJlc3VsdDsKCglpID0gMDsKCXNpZ24gPSAxOwoJcmVzdWx0ID0gMDsKCXdoaWxlIChzdHJbaV0gPT0gJyAnIHx8IHN0cltpXSA9PSAnXHQnIHx8IHN0cltpXSA9PSAnXG4nCgkJfHwgc3RyW2ldID09ICdccicgfHwgc3RyW2ldID09ICdcdicgfHwgc3RyW2ldID09ICdcZicpCgkJaSsrOwoJaWYgKHN0cltpXSA9PSAnLScgfHwgc3RyW2ldID09ICcrJykKCXsKCQlpZiAoc3RyW2ldID09ICctJykKCQkJc2lnbiA9IC0xOwoJCWkrKzsKCX0KCXdoaWxlIChzdHJbaV0gPj0gJzAnICYmIHN0cltpXSA8PSAnOScpCgkJcmVzdWx0ID0gcmVzdWx0ICogMTAgKyAoc3RyW2krK10gLSAnMCcpOwoJcmV0dXJuIChyZXN1bHQgKiBzaWduKTsKfQo=', 'ft_is_power_2': 'aW50CWZ0X2lzX3Bvd2VyXzIodW5zaWduZWQgaW50IG4pCnsKCWlmIChuID09IDApCgkJcmV0dXJuICgwKTsKCXJldHVybiAoKG4gJiAobiAtIDEpKSA9PSAwKTsKfQo=', 'ft_strcmp': 'aW50CWZ0X3N0cmNtcChjaGFyICpzMSwgY2hhciAqczIpCnsKCWludCBpOwoKCWkgPSAwOwoJd2hpbGUgKHMxW2ldICYmIHMxW2ldID09IHMyW2ldKQoJCWkrKzsKCXJldHVybiAoKHVuc2lnbmVkIGNoYXIpczFbaV0gLSAodW5zaWduZWQgY2hhcilzMltpXSk7Cn0K', 'ft_strcspn': 'I2luY2x1ZGUgPHN0ZGRlZi5oPgoKc2l6ZV90CWZ0X3N0cmNzcG4oY29uc3QgY2hhciAqcywgY29uc3QgY2hhciAqcmVqZWN0KQp7CglzaXplX3QgaTsKCXNpemVfdCBqOwoKCWkgPSAwOwoJd2hpbGUgKHNbaV0pCgl7CgkJaiA9IDA7CgkJd2hpbGUgKHJlamVjdFtqXSkKCQl7CgkJCWlmIChzW2ldID09IHJlamVjdFtqXSkKCQkJCXJldHVybiAoaSk7CgkJCWorKzsKCQl9CgkJaSsrOwoJfQoJcmV0dXJuIChpKTsKfQo=', 'ft_strdup': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKY2hhcgkqZnRfc3RyZHVwKGNoYXIgKnNyYykKewoJaW50CQlsZW47CglpbnQJCWk7CgljaGFyCSpkdXA7CgoJbGVuID0gMDsKCXdoaWxlIChzcmNbbGVuXSkKCQlsZW4rKzsKCWR1cCA9IG1hbGxvYyhsZW4gKyAxKTsKCWlmICghZHVwKQoJCXJldHVybiAoTlVMTCk7CglpID0gMDsKCXdoaWxlIChpIDwgbGVuKQoJewoJCWR1cFtpXSA9IHNyY1tpXTsKCQlpKys7Cgl9CglkdXBbaV0gPSAnXDAnOwoJcmV0dXJuIChkdXApOwp9Cg==', 'ft_strpbrk': 'Y2hhcgkqZnRfc3RycGJyayhjb25zdCBjaGFyICpzMSwgY29uc3QgY2hhciAqczIpCnsKCWludCBpOwoJaW50IGo7CgoJaSA9IDA7Cgl3aGlsZSAoczFbaV0pCgl7CgkJaiA9IDA7CgkJd2hpbGUgKHMyW2pdKQoJCXsKCQkJaWYgKHMxW2ldID09IHMyW2pdKQoJCQkJcmV0dXJuICgoY2hhciAqKXMxICsgaSk7CgkJCWorKzsKCQl9CgkJaSsrOwoJfQoJcmV0dXJuICgwKTsKfQo=', 'ft_strrev': 'Y2hhcgkqZnRfc3RycmV2KGNoYXIgKnN0cikKewoJaW50CQlpOwoJaW50CQlqOwoJY2hhcgl0bXA7CgoJaSA9IDA7CglqID0gMDsKCXdoaWxlIChzdHJbal0pCgkJaisrOwoJai0tOwoJd2hpbGUgKGkgPCBqKQoJewoJCXRtcCA9IHN0cltpXTsKCQlzdHJbaV0gPSBzdHJbal07CgkJc3RyW2pdID0gdG1wOwoJCWkrKzsKCQlqLS07Cgl9CglyZXR1cm4gKHN0cik7Cn0K', 'ft_strspn': 'I2luY2x1ZGUgPHN0ZGRlZi5oPgoKc2l6ZV90CWZ0X3N0cnNwbihjb25zdCBjaGFyICpzLCBjb25zdCBjaGFyICphY2NlcHQpCnsKCXNpemVfdAlpOwoJc2l6ZV90CWo7CglpbnQJCWZvdW5kOwoKCWkgPSAwOwoJd2hpbGUgKHNbaV0pCgl7CgkJaiA9IDA7CgkJZm91bmQgPSAwOwoJCXdoaWxlIChhY2NlcHRbal0pCgkJewoJCQlpZiAoc1tpXSA9PSBhY2NlcHRbal0pCgkJCXsKCQkJCWZvdW5kID0gMTsKCQkJCWJyZWFrOwoJCQl9CgkJCWorKzsKCQl9CgkJaWYgKCFmb3VuZCkKCQkJcmV0dXJuIChpKTsKCQlpKys7Cgl9CglyZXR1cm4gKGkpOwp9Cg==', 'inter': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CglpbnQgazsKCWludCBmb3VuZDsKCglpZiAoYWMgPT0gMykKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQlqID0gMDsKCQkJZm91bmQgPSAwOwoJCQl3aGlsZSAoYXZbMl1bal0pCgkJCXsKCQkJCWlmIChhdlsxXVtpXSA9PSBhdlsyXVtqXSkKCQkJCXsKCQkJCQlmb3VuZCA9IDE7CgkJCQkJYnJlYWs7CgkJCQl9CgkJCQlqKys7CgkJCX0KCQkJaWYgKGZvdW5kKQoJCQl7CgkJCQlrID0gMDsKCQkJCXdoaWxlIChrIDwgaSkKCQkJCXsKCQkJCQlpZiAoYXZbMV1ba10gPT0gYXZbMV1baV0pCgkJCQkJewoJCQkJCQlmb3VuZCA9IDA7CgkJCQkJCWJyZWFrOwoJCQkJCX0KCQkJCQlrKys7CgkJCQl9CgkJCX0KCQkJaWYgKGZvdW5kKQoJCQkJd3JpdGUoMSwgJmF2WzFdW2ldLCAxKTsKCQkJaSsrOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo=', 'last_word': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGVuZDsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJCWkrKzsKCQlpLS07CgkJd2hpbGUgKGkgPj0gMCAmJiAoYXZbMV1baV0gPT0gJyAnIHx8IGF2WzFdW2ldID09ICdcdCcpKQoJCQlpLS07CgkJZW5kID0gaTsKCQl3aGlsZSAoaSA+PSAwICYmIGF2WzFdW2ldICE9ICcgJyAmJiBhdlsxXVtpXSAhPSAnXHQnKQoJCQlpLS07CgkJaSsrOwoJCXdoaWxlIChpIDw9IGVuZCkKCQkJd3JpdGUoMSwgJmF2WzFdW2krK10sIDEpOwoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'max': 'aW50CW1heChpbnQgKmFyciwgaW50IGxlbikKewoJaW50IGk7CglpbnQgbTsKCglpZiAobGVuIDw9IDApCgkJcmV0dXJuICgwKTsKCW0gPSBhcnJbMF07CglpID0gMTsKCXdoaWxlIChpIDwgbGVuKQoJewoJCWlmIChhcnJbaV0gPiBtKQoJCQltID0gYXJyW2ldOwoJCWkrKzsKCX0KCXJldHVybiAobSk7Cn0K', 'print_bits': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKdm9pZAlwcmludF9iaXRzKHVuc2lnbmVkIGNoYXIgb2N0ZXQpCnsKCWludAkJaTsKCWNoYXIJYzsKCglpID0gNzsKCXdoaWxlIChpID49IDApCgl7CgkJYyA9ICcwJyArICgob2N0ZXQgPj4gaSkgJiAxKTsKCQl3cml0ZSgxLCAmYywgMSk7CgkJaS0tOwoJfQp9Cg==', 'reverse_bits': 'dW5zaWduZWQgY2hhcglyZXZlcnNlX2JpdHModW5zaWduZWQgY2hhciBvY3RldCkKewoJdW5zaWduZWQgY2hhcglyZXN1bHQ7CglpbnQJCQkJaTsKCglyZXN1bHQgPSAwOwoJaSA9IDA7Cgl3aGlsZSAoaSA8IDgpCgl7CgkJcmVzdWx0ID0gKHJlc3VsdCA8PCAxKSB8IChvY3RldCAmIDEpOwoJCW9jdGV0ID4+PSAxOwoJCWkrKzsKCX0KCXJldHVybiAocmVzdWx0KTsKfQo=', 'snake_to_camel': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJaTsKCWNoYXIJYzsKCWludAkJY2FwX25leHQ7CgoJaWYgKGFjID09IDIpCgl7CgkJaSA9IDA7CgkJY2FwX25leHQgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQl7CgkJCWMgPSBhdlsxXVtpXTsKCQkJaWYgKGMgPT0gJ18nKQoJCQl7CgkJCQljYXBfbmV4dCA9IDE7CgkJCQlpKys7CgkJCQljb250aW51ZTsKCQkJfQoJCQlpZiAoY2FwX25leHQgJiYgYyA+PSAnYScgJiYgYyA8PSAneicpCgkJCXsKCQkJCWMgLT0gMzI7CgkJCQljYXBfbmV4dCA9IDA7CgkJCX0KCQkJd3JpdGUoMSwgJmMsIDEpOwoJCQlpKys7CgkJfQoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'swap_bits': 'dW5zaWduZWQgY2hhcglzd2FwX2JpdHModW5zaWduZWQgY2hhciBvY3RldCkKewoJcmV0dXJuICgob2N0ZXQgPj4gMSAmIDB4NTUpIHwgKG9jdGV0IDw8IDEgJiAweEFBKSk7Cn0K', 'union': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CglpbnQgZm91bmQ7CgoJaWYgKGFjID09IDMpCgl7CgkJaSA9IDA7CgkJd2hpbGUgKGF2WzFdW2ldKQoJCXsKCQkJaiA9IDA7CgkJCWZvdW5kID0gMDsKCQkJd2hpbGUgKGogPCBpKQoJCQl7CgkJCQlpZiAoYXZbMV1bal0gPT0gYXZbMV1baV0pCgkJCQl7CgkJCQkJZm91bmQgPSAxOwoJCQkJCWJyZWFrOwoJCQkJfQoJCQkJaisrOwoJCQl9CgkJCWlmICghZm91bmQpCgkJCQl3cml0ZSgxLCAmYXZbMV1baV0sIDEpOwoJCQlpKys7CgkJfQoJCWkgPSAwOwoJCXdoaWxlIChhdlsyXVtpXSkKCQl7CgkJCWogPSAwOwoJCQlmb3VuZCA9IDA7CgkJCXdoaWxlIChhdlsxXVtqXSkKCQkJewoJCQkJaWYgKGF2WzFdW2pdID09IGF2WzJdW2ldKQoJCQkJewoJCQkJCWZvdW5kID0gMTsKCQkJCQlicmVhazsKCQkJCX0KCQkJCWorKzsKCQkJfQoJCQlpZiAoIWZvdW5kKQoJCQl7CgkJCQlqID0gMDsKCQkJCXdoaWxlIChqIDwgaSkKCQkJCXsKCQkJCQlpZiAoYXZbMl1bal0gPT0gYXZbMl1baV0pCgkJCQkJewoJCQkJCQlmb3VuZCA9IDE7CgkJCQkJCWJyZWFrOwoJCQkJCX0KCQkJCQlqKys7CgkJCQl9CgkJCX0KCQkJaWYgKCFmb3VuZCkKCQkJCXdyaXRlKDEsICZhdlsyXVtpXSwgMSk7CgkJCWkrKzsKCQl9Cgl9Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'wdmatch': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CgoJaWYgKGFjID09IDMpCgl7CgkJaSA9IDA7CgkJaiA9IDA7CgkJd2hpbGUgKGF2WzFdW2ldICYmIGF2WzJdW2pdKQoJCXsKCQkJaWYgKGF2WzFdW2ldID09IGF2WzJdW2pdKQoJCQkJaSsrOwoJCQlqKys7CgkJfQoJCWlmICghYXZbMV1baV0pCgkJewoJCQlpID0gMDsKCQkJd2hpbGUgKGF2WzFdW2ldKQoJCQkJd3JpdGUoMSwgJmF2WzFdW2krK10sIDEpOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo='}, 'level3': {'add_prime_sum': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKc3RhdGljIGludAlpc19wcmltZShpbnQgbikKewoJaW50IGk7CgoJaWYgKG4gPCAyKQoJCXJldHVybiAoMCk7CglpID0gMjsKCXdoaWxlIChpICogaSA8PSBuKQoJewoJCWlmIChuICUgaSA9PSAwKQoJCQlyZXR1cm4gKDApOwoJCWkrKzsKCX0KCXJldHVybiAoMSk7Cn0KCnN0YXRpYyB2b2lkCXB1dF9uYnIoaW50IG4pCnsKCWNoYXIgYzsKCglpZiAobiA+PSAxMCkKCQlwdXRfbmJyKG4gLyAxMCk7CgljID0gJzAnICsgbiAlIDEwOwoJd3JpdGUoMSwgJmMsIDEpOwp9CgpzdGF0aWMgaW50CWZ0X2F0b2koY29uc3QgY2hhciAqc3RyKQp7CglpbnQgaTsKCWludCBzaWduOwoJaW50IHJlc3VsdDsKCglpID0gMDsKCXNpZ24gPSAxOwoJcmVzdWx0ID0gMDsKCXdoaWxlIChzdHJbaV0gPT0gJyAnIHx8IHN0cltpXSA9PSAnXHQnIHx8IHN0cltpXSA9PSAnXG4nCgkJfHwgc3RyW2ldID09ICdccicgfHwgc3RyW2ldID09ICdcdicgfHwgc3RyW2ldID09ICdcZicpCgkJaSsrOwoJaWYgKHN0cltpXSA9PSAnLScgfHwgc3RyW2ldID09ICcrJykKCXsKCQlpZiAoc3RyW2ldID09ICctJykKCQkJc2lnbiA9IC0xOwoJCWkrKzsKCX0KCXdoaWxlIChzdHJbaV0gPj0gJzAnICYmIHN0cltpXSA8PSAnOScpCgkJcmVzdWx0ID0gcmVzdWx0ICogMTAgKyAoc3RyW2krK10gLSAnMCcpOwoJcmV0dXJuIChyZXN1bHQgKiBzaWduKTsKfQoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IG47CglpbnQgc3VtOwoKCWlmIChhYyAhPSAyKQoJewoJCXdyaXRlKDEsICIwXG4iLCAyKTsKCQlyZXR1cm4gKDApOwoJfQoJbiA9IGZ0X2F0b2koYXZbMV0pOwoJaWYgKG4gPD0gMCkKCXsKCQl3cml0ZSgxLCAiMFxuIiwgMik7CgkJcmV0dXJuICgwKTsKCX0KCXN1bSA9IDA7CglpID0gMjsKCXdoaWxlIChpIDw9IG4pCgl7CgkJaWYgKGlzX3ByaW1lKGkpKQoJCQlzdW0gKz0gaTsKCQlpKys7Cgl9CglwdXRfbmJyKHN1bSk7Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'epur_str': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IHNwYWNlOwoJaW50IHN0YXJ0ZWQ7CgoJaWYgKGFjID09IDIpCgl7CgkJaSA9IDA7CgkJc3BhY2UgPSAwOwoJCXN0YXJ0ZWQgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQl7CgkJCWlmIChhdlsxXVtpXSA9PSAnICcgfHwgYXZbMV1baV0gPT0gJ1x0JykKCQkJCXNwYWNlID0gMTsKCQkJZWxzZQoJCQl7CgkJCQlpZiAoc3BhY2UgJiYgc3RhcnRlZCkKCQkJCQl3cml0ZSgxLCAiICIsIDEpOwoJCQkJd3JpdGUoMSwgJmF2WzFdW2ldLCAxKTsKCQkJCXN0YXJ0ZWQgPSAxOwoJCQkJc3BhY2UgPSAwOwoJCQl9CgkJCWkrKzsKCQl9Cgl9Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'expand_str': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CWlzX3NlcChjaGFyIGMpCnsKCXJldHVybiAoYyA9PSAnICcgfHwgYyA9PSAnXHQnKTsKfQoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGZpcnN0X3dvcmQ7CglpbnQgaW5fd29yZDsKCglpZiAoYWMgPT0gMikKCXsKCQlpID0gMDsKCQlmaXJzdF93b3JkID0gMTsKCQlpbl93b3JkID0gMDsKCQl3aGlsZSAoYXZbMV1baV0pCgkJewoJCQlpZiAoIWlzX3NlcChhdlsxXVtpXSkpCgkJCXsKCQkJCWlmICghaW5fd29yZCAmJiAhZmlyc3Rfd29yZCkKCQkJCQl3cml0ZSgxLCAiICAgIiwgMyk7CgkJCQl3cml0ZSgxLCAmYXZbMV1baV0sIDEpOwoJCQkJaW5fd29yZCA9IDE7CgkJCQlmaXJzdF93b3JkID0gMDsKCQkJfQoJCQllbHNlCgkJCQlpbl93b3JkID0gMDsKCQkJaSsrOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo=', 'ft_atoi_base': 'aW50CWZ0X2F0b2lfYmFzZShjb25zdCBjaGFyICpzdHIsIGludCBiYXNlKQp7CglpbnQgaTsKCWludCBzaWduOwoJaW50IHJlc3VsdDsKCWludCBkaWdpdDsKCglpID0gMDsKCXNpZ24gPSAxOwoJcmVzdWx0ID0gMDsKCXdoaWxlIChzdHJbaV0gPT0gJyAnIHx8IHN0cltpXSA9PSAnXHQnIHx8IHN0cltpXSA9PSAnXG4nCgkJfHwgc3RyW2ldID09ICdccicgfHwgc3RyW2ldID09ICdcdicgfHwgc3RyW2ldID09ICdcZicpCgkJaSsrOwoJaWYgKHN0cltpXSA9PSAnLScgfHwgc3RyW2ldID09ICcrJykKCXsKCQlpZiAoc3RyW2ldID09ICctJykKCQkJc2lnbiA9IC0xOwoJCWkrKzsKCX0KCXdoaWxlIChzdHJbaV0pCgl7CgkJaWYgKHN0cltpXSA+PSAnMCcgJiYgc3RyW2ldIDw9ICc5JykKCQkJZGlnaXQgPSBzdHJbaV0gLSAnMCc7CgkJZWxzZSBpZiAoc3RyW2ldID49ICdhJyAmJiBzdHJbaV0gPD0gJ2YnKQoJCQlkaWdpdCA9IHN0cltpXSAtICdhJyArIDEwOwoJCWVsc2UgaWYgKHN0cltpXSA+PSAnQScgJiYgc3RyW2ldIDw9ICdGJykKCQkJZGlnaXQgPSBzdHJbaV0gLSAnQScgKyAxMDsKCQllbHNlCgkJCWJyZWFrOwoJCWlmIChkaWdpdCA+PSBiYXNlKQoJCQlicmVhazsKCQlyZXN1bHQgPSByZXN1bHQgKiBiYXNlICsgZGlnaXQ7CgkJaSsrOwoJfQoJcmV0dXJuIChyZXN1bHQgKiBzaWduKTsKfQo=', 'ft_list_size': 'I2luY2x1ZGUgImZ0X2xpc3QuaCIKCmludAlmdF9saXN0X3NpemUodF9saXN0ICpiZWdpbl9saXN0KQp7CglpbnQgc2l6ZTsKCglzaXplID0gMDsKCXdoaWxlIChiZWdpbl9saXN0KQoJewoJCXNpemUrKzsKCQliZWdpbl9saXN0ID0gYmVnaW5fbGlzdC0+bmV4dDsKCX0KCXJldHVybiAoc2l6ZSk7Cn0K', 'ft_range': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKaW50CSpmdF9yYW5nZShpbnQgc3RhcnQsIGludCBlbmQpCnsKCWludAkqYXJyOwoJaW50CWxlbjsKCWludAlzdGVwOwoJaW50CWk7CgoJc3RlcCA9IChzdGFydCA8PSBlbmQpID8gMSA6IC0xOwoJbGVuID0gKHN0YXJ0IDw9IGVuZCkgPyAoZW5kIC0gc3RhcnQgKyAxKSA6IChzdGFydCAtIGVuZCArIDEpOwoJYXJyID0gbWFsbG9jKGxlbiAqIHNpemVvZihpbnQpKTsKCWlmICghYXJyKQoJCXJldHVybiAoTlVMTCk7CglpID0gMDsKCXdoaWxlIChpIDwgbGVuKQoJewoJCWFycltpXSA9IHN0YXJ0ICsgaSAqIHN0ZXA7CgkJaSsrOwoJfQoJcmV0dXJuIChhcnIpOwp9Cg==', 'ft_rrange': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKaW50CSpmdF9ycmFuZ2UoaW50IHN0YXJ0LCBpbnQgZW5kKQp7CglpbnQJKmFycjsKCWludAlsZW47CglpbnQJaTsKCWludAljdXI7CgoJbGVuID0gKHN0YXJ0IDw9IGVuZCkgPyAoZW5kIC0gc3RhcnQgKyAxKSA6IChzdGFydCAtIGVuZCArIDEpOwoJYXJyID0gbWFsbG9jKGxlbiAqIHNpemVvZihpbnQpKTsKCWlmICghYXJyKQoJCXJldHVybiAoTlVMTCk7CgljdXIgPSBlbmQ7CglpID0gMDsKCXdoaWxlIChpIDwgbGVuKQoJewoJCWFycltpXSA9IGN1cjsKCQlpZiAoc3RhcnQgPD0gZW5kKQoJCQljdXItLTsKCQllbHNlCgkJCWN1cisrOwoJCWkrKzsKCX0KCXJldHVybiAoYXJyKTsKfQo=', 'hidenp': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CgoJaWYgKGFjID09IDMpCgl7CgkJaSA9IDA7CgkJaiA9IDA7CgkJd2hpbGUgKGF2WzFdW2ldICYmIGF2WzJdW2pdKQoJCXsKCQkJaWYgKGF2WzFdW2ldID09IGF2WzJdW2pdKQoJCQkJaSsrOwoJCQlqKys7CgkJfQoJCWlmICghYXZbMV1baV0pCgkJCXdyaXRlKDEsICIxXG4iLCAyKTsKCQllbHNlCgkJCXdyaXRlKDEsICIwXG4iLCAyKTsKCX0KCWVsc2UKCQl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'lcm': 'dW5zaWduZWQgaW50CWxjbSh1bnNpZ25lZCBpbnQgYSwgdW5zaWduZWQgaW50IGIpCnsKCXVuc2lnbmVkIGludCB4OwoJdW5zaWduZWQgaW50IHk7Cgl1bnNpZ25lZCBpbnQgdG1wOwoJdW5zaWduZWQgaW50IGdjZDsKCglpZiAoYSA9PSAwIHx8IGIgPT0gMCkKCQlyZXR1cm4gKDApOwoJeCA9IGE7Cgl5ID0gYjsKCXdoaWxlICh5ICE9IDApCgl7CgkJdG1wID0geTsKCQl5ID0geCAlIHk7CgkJeCA9IHRtcDsKCX0KCWdjZCA9IHg7CglyZXR1cm4gKGEgLyBnY2QgKiBiKTsKfQo=', 'paramsum': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKdm9pZAlwdXRfbmJyKGludCBuKQp7CgljaGFyIGM7CgoJaWYgKG4gPj0gMTApCgkJcHV0X25icihuIC8gMTApOwoJYyA9ICcwJyArIG4gJSAxMDsKCXdyaXRlKDEsICZjLCAxKTsKfQoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCSh2b2lkKWF2OwoJcHV0X25icihhYyAtIDEpOwoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'pgcd': 'I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdGRsaWIuaD4KCmludAltYWluKGludCBhYywgY2hhciAqKmF2KQp7Cgl1bnNpZ25lZCBpbnQgYTsKCXVuc2lnbmVkIGludCBiOwoJdW5zaWduZWQgaW50IHRtcDsKCglpZiAoYWMgIT0gMykKCXsKCQlwcmludGYoIlxuIik7CgkJcmV0dXJuICgwKTsKCX0KCWEgPSBhdG9pKGF2WzFdKTsKCWIgPSBhdG9pKGF2WzJdKTsKCXdoaWxlIChiICE9IDApCgl7CgkJdG1wID0gYjsKCQliID0gYSAlIGI7CgkJYSA9IHRtcDsKCX0KCXByaW50ZigiJXVcbiIsIGEpOwoJcmV0dXJuICgwKTsKfQo=', 'print_hex': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKc3RhdGljIHZvaWQJcHJpbnRfaGV4KHVuc2lnbmVkIGludCBuKQp7CgljaGFyICpoZXggPSAiMDEyMzQ1Njc4OWFiY2RlZiI7CgoJaWYgKG4gPj0gMTYpCgkJcHJpbnRfaGV4KG4gLyAxNik7Cgl3cml0ZSgxLCAmaGV4W24gJSAxNl0sIDEpOwp9CgpzdGF0aWMgaW50CWZ0X2F0b2koY29uc3QgY2hhciAqc3RyKQp7CglpbnQgaTsKCWludCByZXN1bHQ7CgoJaSA9IDA7CglyZXN1bHQgPSAwOwoJd2hpbGUgKHN0cltpXSA+PSAnMCcgJiYgc3RyW2ldIDw9ICc5JykKCQlyZXN1bHQgPSByZXN1bHQgKiAxMCArIChzdHJbaSsrXSAtICcwJyk7CglyZXR1cm4gKHJlc3VsdCk7Cn0KCmludAltYWluKGludCBhYywgY2hhciAqKmF2KQp7CglpZiAoYWMgPT0gMikKCQlwcmludF9oZXgoKHVuc2lnbmVkIGludClmdF9hdG9pKGF2WzFdKSk7Cgl3cml0ZSgxLCAiXG4iLCAxKTsKCXJldHVybiAoMCk7Cn0K', 'rstr_capitalizer': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJYTsKCWludAkJaTsKCWNoYXIJYzsKCglpZiAoYWMgPT0gMSkKCXsKCQl3cml0ZSgxLCAiXG4iLCAxKTsKCQlyZXR1cm4gKDApOwoJfQoJYSA9IDE7Cgl3aGlsZSAoYSA8IGFjKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlthXVtpXSkKCQl7CgkJCWMgPSBhdlthXVtpXTsKCQkJaWYgKChjID49ICdhJyAmJiBjIDw9ICd6JykgfHwgKGMgPj0gJ0EnICYmIGMgPD0gJ1onKSkKCQkJewoJCQkJaWYgKGF2W2FdW2kgKyAxXSA9PSAnICcgfHwgYXZbYV1baSArIDFdID09ICdcdCcKCQkJCQl8fCBhdlthXVtpICsgMV0gPT0gJ1wwJykKCQkJCXsKCQkJCQlpZiAoYyA+PSAnYScgJiYgYyA8PSAneicpCgkJCQkJCWMgLT0gMzI7CgkJCQl9CgkJCQllbHNlCgkJCQl7CgkJCQkJaWYgKGMgPj0gJ0EnICYmIGMgPD0gJ1onKQoJCQkJCQljICs9IDMyOwoJCQkJfQoJCQl9CgkJCXdyaXRlKDEsICZjLCAxKTsKCQkJaSsrOwoJCX0KCQl3cml0ZSgxLCAiXG4iLCAxKTsKCQlhKys7Cgl9CglyZXR1cm4gKDApOwp9Cg==', 'str_capitalizer': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludAkJYTsKCWludAkJaTsKCWNoYXIJYzsKCWludAkJbmV3X3dvcmQ7CgoJaWYgKGFjID09IDEpCgl7CgkJd3JpdGUoMSwgIlxuIiwgMSk7CgkJcmV0dXJuICgwKTsKCX0KCWEgPSAxOwoJd2hpbGUgKGEgPCBhYykKCXsKCQlpID0gMDsKCQluZXdfd29yZCA9IDE7CgkJd2hpbGUgKGF2W2FdW2ldKQoJCXsKCQkJYyA9IGF2W2FdW2ldOwoJCQlpZiAoYyA9PSAnICcgfHwgYyA9PSAnXHQnIHx8IGMgPT0gJ1xuJykKCQkJCW5ld193b3JkID0gMTsKCQkJZWxzZSBpZiAobmV3X3dvcmQpCgkJCXsKCQkJCWlmIChjID49ICdhJyAmJiBjIDw9ICd6JykKCQkJCQljIC09IDMyOwoJCQkJbmV3X3dvcmQgPSAwOwoJCQl9CgkJCWVsc2UKCQkJewoJCQkJaWYgKGMgPj0gJ0EnICYmIGMgPD0gJ1onKQoJCQkJCWMgKz0gMzI7CgkJCX0KCQkJd3JpdGUoMSwgJmMsIDEpOwoJCQlpKys7CgkJfQoJCXdyaXRlKDEsICJcbiIsIDEpOwoJCWErKzsKCX0KCXJldHVybiAoMCk7Cn0K', 'tab_mult': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKc3RhdGljIHZvaWQJcHV0X25icihpbnQgbikKewoJY2hhciBjOwoKCWlmIChuID49IDEwKQoJCXB1dF9uYnIobiAvIDEwKTsKCWMgPSAnMCcgKyBuICUgMTA7Cgl3cml0ZSgxLCAmYywgMSk7Cn0KCnN0YXRpYyBpbnQJZnRfYXRvaShjb25zdCBjaGFyICpzdHIpCnsKCWludCBpOwoJaW50IHJlc3VsdDsKCglpID0gMDsKCXJlc3VsdCA9IDA7Cgl3aGlsZSAoc3RyW2ldID49ICcwJyAmJiBzdHJbaV0gPD0gJzknKQoJCXJlc3VsdCA9IHJlc3VsdCAqIDEwICsgKHN0cltpKytdIC0gJzAnKTsKCXJldHVybiAocmVzdWx0KTsKfQoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBuOwoJaW50IGk7CgoJaWYgKGFjICE9IDIpCgl7CgkJd3JpdGUoMSwgIlxuIiwgMSk7CgkJcmV0dXJuICgwKTsKCX0KCW4gPSBmdF9hdG9pKGF2WzFdKTsKCWkgPSAxOwoJd2hpbGUgKGkgPD0gOSkKCXsKCQlwdXRfbmJyKGkpOwoJCXdyaXRlKDEsICIgeCAiLCAzKTsKCQlwdXRfbmJyKG4pOwoJCXdyaXRlKDEsICIgPSAiLCAzKTsKCQlwdXRfbmJyKGkgKiBuKTsKCQl3cml0ZSgxLCAiXG4iLCAxKTsKCQlpKys7Cgl9CglyZXR1cm4gKDApOwp9Cg=='}, 'level4': {'flood_fill': 'I2luY2x1ZGUgInRfcG9pbnQuaCIKCnN0YXRpYyB2b2lkCWZpbGwoY2hhciAqKnRhYiwgdF9wb2ludCBzaXplLCB0X3BvaW50IHBvcywgY2hhciBjKQp7Cgl0X3BvaW50IG5leHQ7CgoJaWYgKHBvcy54IDwgMCB8fCBwb3MueCA+PSBzaXplLnggfHwgcG9zLnkgPCAwIHx8IHBvcy55ID49IHNpemUueSkKCQlyZXR1cm4gOwoJaWYgKHRhYltwb3MueV1bcG9zLnhdICE9IGMpCgkJcmV0dXJuIDsKCXRhYltwb3MueV1bcG9zLnhdID0gJ0YnOwoJbmV4dCA9IHBvczsKCW5leHQueCArPSAxOwoJZmlsbCh0YWIsIHNpemUsIG5leHQsIGMpOwoJbmV4dCA9IHBvczsKCW5leHQueCAtPSAxOwoJZmlsbCh0YWIsIHNpemUsIG5leHQsIGMpOwoJbmV4dCA9IHBvczsKCW5leHQueSArPSAxOwoJZmlsbCh0YWIsIHNpemUsIG5leHQsIGMpOwoJbmV4dCA9IHBvczsKCW5leHQueSAtPSAxOwoJZmlsbCh0YWIsIHNpemUsIG5leHQsIGMpOwp9Cgp2b2lkCWZsb29kX2ZpbGwoY2hhciAqKnRhYiwgdF9wb2ludCBzaXplLCB0X3BvaW50IGJlZ2luKQp7CglmaWxsKHRhYiwgc2l6ZSwgYmVnaW4sIHRhYltiZWdpbi55XVtiZWdpbi54XSk7Cn0K', 'fprime': 'I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdGRsaWIuaD4KCmludAltYWluKGludCBhYywgY2hhciAqKmF2KQp7CglpbnQgbjsKCWludCBpOwoJaW50IGZpcnN0OwoKCWlmIChhYyAhPSAyKQoJewoJCXByaW50ZigiXG4iKTsKCQlyZXR1cm4gKDApOwoJfQoJbiA9IGF0b2koYXZbMV0pOwoJaSA9IDI7CglmaXJzdCA9IDE7CglpZiAobiA9PSAxKQoJewoJCXByaW50ZigiMVxuIik7CgkJcmV0dXJuICgwKTsKCX0KCXdoaWxlIChuID4gMSkKCXsKCQlpZiAobiAlIGkgPT0gMCkKCQl7CgkJCWlmICghZmlyc3QpCgkJCQlwcmludGYoIioiKTsKCQkJcHJpbnRmKCIlZCIsIGkpOwoJCQlmaXJzdCA9IDA7CgkJCW4gLz0gaTsKCQl9CgkJZWxzZQoJCQlpKys7Cgl9CglwcmludGYoIlxuIik7CglyZXR1cm4gKDApOwp9Cg==', 'ft_itoa': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKY2hhcgkqZnRfaXRvYShpbnQgbmJyKQp7CgljaGFyCSpzdHI7Cglsb25nCW47CglpbnQJCWxlbjsKCWxvbmcJdG1wOwoKCW4gPSAobG9uZyluYnI7CglsZW4gPSAobiA8PSAwKSA/IDEgOiAwOwoJdG1wID0gKG4gPCAwKSA/IC1uIDogbjsKCXdoaWxlICh0bXAgPiAwKQoJewoJCWxlbisrOwoJCXRtcCAvPSAxMDsKCX0KCXN0ciA9IG1hbGxvYyhsZW4gKyAxKTsKCWlmICghc3RyKQoJCXJldHVybiAoTlVMTCk7CglzdHJbbGVuXSA9ICdcMCc7CglpZiAobiA9PSAwKQoJewoJCXN0clswXSA9ICcwJzsKCQlyZXR1cm4gKHN0cik7Cgl9CglpZiAobiA8IDApCgl7CgkJc3RyWzBdID0gJy0nOwoJCW4gPSAtbjsKCX0KCXdoaWxlIChuID4gMCkKCXsKCQlzdHJbLS1sZW5dID0gJzAnICsgbiAlIDEwOwoJCW4gLz0gMTA7Cgl9CglyZXR1cm4gKHN0cik7Cn0K', 'ft_list_foreach': 'I2luY2x1ZGUgImZ0X2xpc3QuaCIKCnZvaWQJZnRfbGlzdF9mb3JlYWNoKHRfbGlzdCAqYmVnaW5fbGlzdCwgdm9pZCAoKmYpKHZvaWQgKikpCnsKCXdoaWxlIChiZWdpbl9saXN0KQoJewoJCWYoYmVnaW5fbGlzdC0+ZGF0YSk7CgkJYmVnaW5fbGlzdCA9IGJlZ2luX2xpc3QtPm5leHQ7Cgl9Cn0K', 'ft_list_remove_if': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKdHlwZWRlZiBzdHJ1Y3Qgc19saXN0CnsKCXN0cnVjdCBzX2xpc3QJKm5leHQ7Cgl2b2lkCQkJKmRhdGE7Cn0JdF9saXN0OwoKdm9pZAlmdF9saXN0X3JlbW92ZV9pZih0X2xpc3QgKipiZWdpbl9saXN0LCB2b2lkICpkYXRhX3JlZiwgaW50ICgqY21wKSgpKQp7Cgl0X2xpc3QJKmN1cnI7Cgl0X2xpc3QJKnByZXY7Cgl0X2xpc3QJKm5leHQ7CgoJcHJldiA9IE5VTEw7CgljdXJyID0gKmJlZ2luX2xpc3Q7Cgl3aGlsZSAoY3VycikKCXsKCQluZXh0ID0gY3Vyci0+bmV4dDsKCQlpZiAoY21wKGN1cnItPmRhdGEsIGRhdGFfcmVmKSA9PSAwKQoJCXsKCQkJaWYgKHByZXYpCgkJCQlwcmV2LT5uZXh0ID0gbmV4dDsKCQkJZWxzZQoJCQkJKmJlZ2luX2xpc3QgPSBuZXh0OwoJCQlmcmVlKGN1cnIpOwoJCX0KCQllbHNlCgkJCXByZXYgPSBjdXJyOwoJCWN1cnIgPSBuZXh0OwoJfQp9Cg==', 'ft_split': 'I2luY2x1ZGUgPHN0ZGxpYi5oPgoKc3RhdGljIGludAlpc19zZXAoY2hhciBjKQp7CglyZXR1cm4gKGMgPT0gJyAnIHx8IGMgPT0gJ1x0JyB8fCBjID09ICdcbicpOwp9CgpzdGF0aWMgaW50CWNvdW50X3dvcmRzKGNoYXIgKnN0cikKewoJaW50IGNvdW50OwoJaW50IGluX3dvcmQ7CgoJY291bnQgPSAwOwoJaW5fd29yZCA9IDA7Cgl3aGlsZSAoKnN0cikKCXsKCQlpZiAoaXNfc2VwKCpzdHIpKQoJCQlpbl93b3JkID0gMDsKCQllbHNlIGlmICghaW5fd29yZCkKCQl7CgkJCWluX3dvcmQgPSAxOwoJCQljb3VudCsrOwoJCX0KCQlzdHIrKzsKCX0KCXJldHVybiAoY291bnQpOwp9CgpzdGF0aWMgaW50CXdvcmRfbGVuKGNoYXIgKnN0cikKewoJaW50IGxlbjsKCglsZW4gPSAwOwoJd2hpbGUgKHN0cltsZW5dICYmICFpc19zZXAoc3RyW2xlbl0pKQoJCWxlbisrOwoJcmV0dXJuIChsZW4pOwp9CgpjaGFyCSoqZnRfc3BsaXQoY2hhciAqc3RyKQp7CgljaGFyCSoqcmVzdWx0OwoJaW50CQl3b3JkczsKCWludAkJaTsKCWludAkJajsKCWludAkJbGVuOwoKCXdvcmRzID0gY291bnRfd29yZHMoc3RyKTsKCXJlc3VsdCA9IG1hbGxvYygod29yZHMgKyAxKSAqIHNpemVvZihjaGFyICopKTsKCWlmICghcmVzdWx0KQoJCXJldHVybiAoTlVMTCk7CglpID0gMDsKCXdoaWxlICgqc3RyKQoJewoJCWlmIChpc19zZXAoKnN0cikpCgkJewoJCQlzdHIrKzsKCQkJY29udGludWU7CgkJfQoJCWxlbiA9IHdvcmRfbGVuKHN0cik7CgkJcmVzdWx0W2ldID0gbWFsbG9jKGxlbiArIDEpOwoJCWlmICghcmVzdWx0W2ldKQoJCQlyZXR1cm4gKE5VTEwpOwoJCWogPSAwOwoJCXdoaWxlIChqIDwgbGVuKQoJCQlyZXN1bHRbaV1baisrXSA9ICpzdHIrKzsKCQlyZXN1bHRbaV1bal0gPSAnXDAnOwoJCWkrKzsKCX0KCXJlc3VsdFtpXSA9IE5VTEw7CglyZXR1cm4gKHJlc3VsdCk7Cn0K', 'rev_wstr': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGo7CglpbnQgZW5kOwoKCWlmIChhYyA9PSAyKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSkKCQkJaSsrOwoJCWktLTsKCQl3aGlsZSAoaSA+PSAwKQoJCXsKCQkJd2hpbGUgKGkgPj0gMCAmJiAoYXZbMV1baV0gPT0gJyAnIHx8IGF2WzFdW2ldID09ICdcdCcpKQoJCQkJaS0tOwoJCQlpZiAoaSA8IDApCgkJCQlicmVhazsKCQkJZW5kID0gaTsKCQkJd2hpbGUgKGkgPj0gMCAmJiBhdlsxXVtpXSAhPSAnICcgJiYgYXZbMV1baV0gIT0gJ1x0JykKCQkJCWktLTsKCQkJaiA9IGkgKyAxOwoJCQl3aGlsZSAoaiA8PSBlbmQpCgkJCQl3cml0ZSgxLCAmYXZbMV1baisrXSwgMSk7CgkJCWlmIChpID49IDApCgkJCQl3cml0ZSgxLCAiICIsIDEpOwoJCX0KCX0KCXdyaXRlKDEsICJcbiIsIDEpOwoJcmV0dXJuICgwKTsKfQo=', 'rostring': 'I2luY2x1ZGUgPHVuaXN0ZC5oPgoKaW50CW1haW4oaW50IGFjLCBjaGFyICoqYXYpCnsKCWludCBpOwoJaW50IGZpcnN0X3N0YXJ0OwoJaW50IGZpcnN0X2VuZDsKCWludCByZXN0OwoKCWlmIChhYyA9PSAyKQoJewoJCWkgPSAwOwoJCXdoaWxlIChhdlsxXVtpXSA9PSAnICcgfHwgYXZbMV1baV0gPT0gJ1x0JykKCQkJaSsrOwoJCWZpcnN0X3N0YXJ0ID0gaTsKCQl3aGlsZSAoYXZbMV1baV0gJiYgYXZbMV1baV0gIT0gJyAnICYmIGF2WzFdW2ldICE9ICdcdCcpCgkJCWkrKzsKCQlmaXJzdF9lbmQgPSBpOwoJCXdoaWxlIChhdlsxXVtpXSA9PSAnICcgfHwgYXZbMV1baV0gPT0gJ1x0JykKCQkJaSsrOwoJCXJlc3QgPSBpOwoJCWlmIChhdlsxXVtyZXN0XSkKCQl7CgkJCXdoaWxlIChhdlsxXVtpXSkKCQkJewoJCQkJaWYgKChhdlsxXVtpXSA9PSAnICcgfHwgYXZbMV1baV0gPT0gJ1x0JykKCQkJCQkmJiAoYXZbMV1baSArIDFdID09ICcgJyB8fCBhdlsxXVtpICsgMV0gPT0gJ1x0JwoJCQkJCQl8fCBhdlsxXVtpICsgMV0gPT0gJ1wwJykpCgkJCQl7CgkJCQkJaSsrOwoJCQkJCWNvbnRpbnVlOwoJCQkJfQoJCQkJd3JpdGUoMSwgJmF2WzFdW2krK10sIDEpOwoJCQl9CgkJCXdyaXRlKDEsICIgIiwgMSk7CgkJCWkgPSBmaXJzdF9zdGFydDsKCQkJd2hpbGUgKGkgPCBmaXJzdF9lbmQpCgkJCQl3cml0ZSgxLCAmYXZbMV1baSsrXSwgMSk7CgkJfQoJCWVsc2UKCQl7CgkJCWkgPSBmaXJzdF9zdGFydDsKCQkJd2hpbGUgKGkgPCBmaXJzdF9lbmQpCgkJCQl3cml0ZSgxLCAmYXZbMV1baSsrXSwgMSk7CgkJfQoJfQoJd3JpdGUoMSwgIlxuIiwgMSk7CglyZXR1cm4gKDApOwp9Cg==', 'sort_int_tab': 'dm9pZAlzb3J0X2ludF90YWIoaW50ICp0YWIsIGludCBzaXplKQp7CglpbnQgaTsKCWludCBqOwoJaW50IHRtcDsKCglpID0gMDsKCXdoaWxlIChpIDwgc2l6ZSAtIDEpCgl7CgkJaiA9IDA7CgkJd2hpbGUgKGogPCBzaXplIC0gaSAtIDEpCgkJewoJCQlpZiAodGFiW2pdID4gdGFiW2ogKyAxXSkKCQkJewoJCQkJdG1wID0gdGFiW2pdOwoJCQkJdGFiW2pdID0gdGFiW2ogKyAxXTsKCQkJCXRhYltqICsgMV0gPSB0bXA7CgkJCX0KCQkJaisrOwoJCX0KCQlpKys7Cgl9Cn0K', 'sort_list': 'I2luY2x1ZGUgImxpc3QuaCIKCnRfbGlzdAkqc29ydF9saXN0KHRfbGlzdCAqbHN0LCBpbnQgKCpjbXApKGludCwgaW50KSkKewoJdF9saXN0CSpjdXJyOwoJdm9pZAkqdG1wOwoJaW50CQlzd2FwcGVkOwoKCWlmICghbHN0KQoJCXJldHVybiAoTlVMTCk7CglkbyB7CgkJc3dhcHBlZCA9IDA7CgkJY3VyciA9IGxzdDsKCQl3aGlsZSAoY3Vyci0+bmV4dCkKCQl7CgkJCWlmICghY21wKChpbnQpKGxvbmcpY3Vyci0+ZGF0YSwgKGludCkobG9uZyljdXJyLT5uZXh0LT5kYXRhKSkKCQkJewoJCQkJdG1wID0gY3Vyci0+ZGF0YTsKCQkJCWN1cnItPmRhdGEgPSBjdXJyLT5uZXh0LT5kYXRhOwoJCQkJY3Vyci0+bmV4dC0+ZGF0YSA9IHRtcDsKCQkJCXN3YXBwZWQgPSAxOwoJCQl9CgkJCWN1cnIgPSBjdXJyLT5uZXh0OwoJCX0KCX0gd2hpbGUgKHN3YXBwZWQpOwoJcmV0dXJuIChsc3QpOwp9Cg=='}}  # noqa: E501

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EXAM_DURATION = 3 * 3600  # 3 heures
BASE_DIR = Path(__file__).parent
EXAMS_DIR = BASE_DIR / "exams"
SUBJECTS_DIR = BASE_DIR / "subjects"
RENDER_DIR = BASE_DIR / "render"
TRACES_DIR = BASE_DIR / "traces"
TESTER_DIR = BASE_DIR / "exams" / ".tester"
SOLUTIONS_DIR = BASE_DIR / "solutions"
LEVELS = ["level1", "level2", "level3", "level4"]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
start_time = 0.0
current_level = 0
score = 0          # points gagnés via grademe uniquement (pas les skips)
current_subject = None  # Path to the active .txt file
time_expired = False
debug_mode = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def format_time(seconds: float) -> str:
    s = abs(int(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def elapsed() -> float:
    return time.time() - start_time


def remaining() -> float:
    return EXAM_DURATION - elapsed()


def clear_dir(path: Path):
    for f in path.iterdir():
        if f.is_file() and f.name != ".gitkeep":
            f.unlink()


def _read_line_with_timer() -> str:
    """
    Lit une ligne sur stdin en affichant un countdown live.
    Utilise le mode raw + select pour mettre à jour le timer
    chaque seconde sans bloquer la saisie.
    """
    buf: list[str] = []
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def _draw():
        t = format_time(max(0.0, remaining()))
        prefix = f"[DEBUG | {t}]" if debug_mode else f"[{t}]"
        sys.stdout.write(f"\r\033[K{prefix} > {''.join(buf)}")
        sys.stdout.flush()

    try:
        tty.setraw(fd)
        _draw()
        while True:
            ready, _, _ = select.select([sys.stdin], [], [], 1.0)
            if not ready:
                _draw()   # mise à jour du timer
                continue
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return "".join(buf)
            elif ch in ("\x7f", "\x08"):   # Backspace
                if buf:
                    buf.pop()
            elif ch == "\x03":             # Ctrl-C
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise KeyboardInterrupt
            elif ch == "\x04":             # Ctrl-D / EOF
                sys.stdout.write("\n")
                sys.stdout.flush()
                raise EOFError
            elif ch.isprintable():
                buf.append(ch)
            _draw()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# ---------------------------------------------------------------------------
# Subject selection
# ---------------------------------------------------------------------------

def select_subject(level_name: str) -> Path | None:
    global current_subject
    level_dir = EXAMS_DIR / level_name
    subjects = list(level_dir.glob("*.txt"))
    if not subjects:
        print(f"[ERROR] Aucun sujet disponible pour {level_name}")
        return None
    chosen = random.choice(subjects)
    clear_dir(SUBJECTS_DIR)
    shutil.copy(chosen, SUBJECTS_DIR / chosen.name)
    current_subject = chosen
    return chosen


# ---------------------------------------------------------------------------
# Subject parsing
# ---------------------------------------------------------------------------

def get_expected_files(subject_path: Path) -> list[str]:
    """Return the list of files the student must produce."""
    with open(subject_path) as f:
        for line in f:
            if line.startswith("Expected files"):
                return [x for x in line.split(":", 1)[1].strip().split() if x]
    return []


def parse_examples(subject_path: Path) -> list[tuple[str, str]]:
    """
    Extract (command, expected_output) pairs from the $> blocks.

    Handles:
      - "| cat -e"  → stripped from command, '$' at line-end → '\n'
      - other pipes → kept in command, run via shell, output compared as-is
    """
    examples = []
    with open(subject_path) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip("\n").lstrip()

        if stripped.startswith("$> ") and len(stripped) > 3:
            cmd_str = stripped[3:]
            has_cat_e = "| cat -e" in cmd_str

            if has_cat_e:
                cmd_str = cmd_str[: cmd_str.index("| cat -e")].rstrip()

            # Collect expected-output lines until blank line or next "$>"
            expected_parts = []
            i += 1
            while i < len(lines):
                nxt = lines[i].rstrip("\n")
                if nxt.lstrip().startswith("$>") or nxt == "":
                    break
                expected_parts.append(nxt)
                i += 1

            # Replace "(newline only)" marker with empty string
            expected_parts = [
                "" if p.strip() == "(newline only)" else p
                for p in expected_parts
            ]

            # Build expected string
            if has_cat_e:
                expected = "".join(
                    (p[:-1] + "\n") if p.endswith("$") else (p + "\n")
                    for p in expected_parts
                )
            else:
                expected = "\n".join(expected_parts) + "\n"

            examples.append((cmd_str.strip(), expected))
        else:
            i += 1

    return examples


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------

def compile_submission(
    expected_files: list[str], subject_name: str, as_binary: bool
) -> tuple[bool, str]:
    """
    Compile .c files from render/.
    as_binary=True  → link into an executable
    as_binary=False → compile only (-c flag, syntax check)

    Returns (success, binary_path_or_error_message).
    """
    c_files = []
    for fname in expected_files:
        fpath = RENDER_DIR / fname
        if not fpath.exists():
            return False, f"Fichier manquant : render/{fname}"
        if fname.endswith(".c"):
            c_files.append(str(fpath))

    if not c_files:
        return True, ""   # header-only

    if as_binary:
        binary = str(RENDER_DIR / subject_name)
        cmd = (
            ["cc", "-Wall", "-Wextra", "-Werror",
             f"-I{RENDER_DIR}", f"-I{TESTER_DIR}"]
            + c_files + ["-o", binary]
        )
    else:
        binary = ""
        cmd = (
            ["cc", "-Wall", "-Wextra", "-Werror", "-c",
             f"-I{RENDER_DIR}", f"-I{TESTER_DIR}"]
            + c_files
        )

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, f"Erreur de compilation :\n{proc.stderr.strip()}"
    return True, binary


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

def run_test(binary: str, cmd_str: str, expected: str) -> tuple[bool, str]:
    """
    Run one example command and return (passed, actual_output).

    If the command contains a pipe other than '| cat -e' (already stripped),
    run via shell with the binary path substituted; otherwise exec directly.
    """
    binary_name = Path(binary).name
    # Replace ./name or name at the start of the command with the full path
    safe_binary = binary.replace("'", "'\\''")

    if "|" in cmd_str:
        # Run via shell (e.g. "| head -N")
        shell_cmd = cmd_str.replace(f"./{binary_name}", f"'{safe_binary}'", 1)
        if shell_cmd == cmd_str:
            shell_cmd = cmd_str.replace(binary_name, f"'{safe_binary}'", 1)
        try:
            proc = subprocess.run(shell_cmd, shell=True, capture_output=True,
                                  text=True, timeout=5)
            actual = proc.stdout
        except subprocess.TimeoutExpired:
            actual = "[TIMEOUT]\n"
    else:
        try:
            parts = shlex.split(cmd_str)
        except ValueError:
            parts = cmd_str.split()
        if not parts:
            parts = [binary]
        elif parts[0] in (f"./{binary_name}", binary_name):
            parts[0] = binary
        try:
            proc = subprocess.run(parts, capture_output=True, timeout=5)
            actual = proc.stdout.decode('utf-8', errors='replace')
        except subprocess.TimeoutExpired:
            actual = "[TIMEOUT]\n"
        except FileNotFoundError as e:
            actual = f"[NOT FOUND: {e}]\n"

    return actual == expected, actual


def compile_with_tester(
    expected_files: list[str], subject_name: str, tester_path: Path
) -> tuple[bool, str]:
    """Compile function files + test main into a binary."""
    c_files = []
    for fname in expected_files:
        fpath = RENDER_DIR / fname
        if not fpath.exists():
            return False, f"Fichier manquant : render/{fname}"
        if fname.endswith(".c"):
            c_files.append(str(fpath))

    if not c_files:
        return False, "Aucun fichier .c trouvé."

    binary = str(RENDER_DIR / f"{subject_name}_tester")
    cmd = (
        ["cc", "-Wall", "-Wextra", "-Werror",
         f"-I{RENDER_DIR}", f"-I{TESTER_DIR}"]
        + c_files + [str(tester_path), "-o", binary]
    )
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, f"Erreur de compilation :\n{proc.stderr.strip()}"
    return True, binary


def run_tester(binary: str) -> tuple[bool, str]:
    """Run tester binary, return (passed, output)."""
    try:
        proc = subprocess.run(
            [binary], capture_output=True, text=True, timeout=10
        )
        output = proc.stdout
        passed = proc.returncode == 0 and "ALL TESTS PASSED" in output
        return passed, output
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT]\n"


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

def _run_grademe() -> bool:
    """Logique de correction — retourne True si réussi. Incrémente score si OK."""
    global score
    if current_subject is None:
        print("[ERROR] Aucun sujet sélectionné.")
        return False
    subject_path = current_subject
    subject_name = subject_path.stem
    print(f"\n--- Correction : {subject_name} ---")

    # 1. Expected files
    expected_files = get_expected_files(subject_path)
    if not expected_files:
        print("[ERROR] Impossible de lire 'Expected files' dans le sujet.")
        return False
    print(f"Fichiers attendus : {', '.join(expected_files)}")

    # 2. Examples → decide if we need a binary
    examples = parse_examples(subject_path)
    as_binary = bool(examples)

    # 3. Compile
    ok, result = compile_submission(expected_files, subject_name, as_binary)
    if not ok:
        print(result)
        trace = TRACES_DIR / f"{subject_name}_trace.txt"
        trace.write_text(result + "\n")
        print(f"Trace : traces/{trace.name}")
        return False
    binary = result
    print("Compilation : OK")

    # 4. No examples → try tester or accept on compilation alone
    if not examples:
        tester_path = TESTER_DIR / f"{subject_name}_test.c"
        if tester_path.exists():
            print(f"Tester trouvé : {tester_path.name}")
            ok, result = compile_with_tester(
                expected_files, subject_name, tester_path
            )
            if not ok:
                print(result)
                trace = TRACES_DIR / f"{subject_name}_trace.txt"
                trace.write_text(result + "\n")
                print(f"Trace : traces/{trace.name}")
                return False
            print("Compilation avec tester : OK")
            passed_tester, output = run_tester(result)
            trace = TRACES_DIR / f"{subject_name}_trace.txt"
            trace.write_text(output)
            print(f"Trace : traces/{trace.name}")
            if passed_tester:
                print("Tous les tests passés → accepté.")
                score += 25
                _advance()
                return True
            else:
                print("Tests échoués. Corrige ton code et retape 'grademe'.")
                print(output)
                return False
        else:
            if not binary:
                print("Exercice header-only : accepté.")
            else:
                print("Pas d'exemples exécutables : compilation OK → accepté.")
            score += 25
            _advance()
            return True

    # 5. Run tests
    passed = 0
    total = len(examples)
    lines = [
        f"Sujet   : {subject_name}",
        f"Date    : {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Tests   : {total}",
        "",
    ]

    for idx, (cmd, expected) in enumerate(examples, 1):
        ok, actual = run_test(binary, cmd, expected)
        status = "OK" if ok else "KO"
        if ok:
            passed += 1
        lines += [
            f"[Test {idx}] $ {cmd}",
            f"  Statut   : {status}",
            f"  Attendu  : {repr(expected)}",
            f"  Obtenu   : {repr(actual)}",
            "",
        ]

    lines.append(f"Score : {passed}/{total}")
    trace = TRACES_DIR / f"{subject_name}_trace.txt"
    trace.write_text("\n".join(lines))

    print(f"Score : {passed}/{total} tests passés")
    print(f"Trace : traces/{trace.name}")

    if passed == total:
        score += 25
        _advance()
        return True
    else:
        print("Corrige ton code et retape 'grademe'.")
        return False


def do_grademe():
    """Wrapper : capture l'output, affiche la bannière en premier."""
    saved_score = score
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        success = _run_grademe()
    finally:
        sys.stdout = old_stdout
    _show_result_banner(success, saved_score)
    print(buf.getvalue(), end="")
    print()


def _show_result_banner(success: bool, points_before: int = -1):
    """Affiche une bannière colorée avec le score et la barre de progression."""
    GREEN = "\033[92m"
    RED   = "\033[91m"
    BOLD  = "\033[1m"
    RESET = "\033[0m"

    if points_before == -1:
        points_before = score
    if success:
        points_after = points_before + 25
        color = GREEN
        icon  = "✓"
        title = "NIVEAU VALIDÉ"
        pts   = "+25 points"
    else:
        points_after = points_before
        color = RED
        icon  = "✗"
        title = "NIVEAU ÉCHOUÉ"
        pts   = "+0 points"

    filled = points_after // 5          # 20 blocs = 100 pts
    bar = "█" * filled + "░" * (20 - filled)

    W = 56  # largeur intérieure de la boîte
    line1 = f"  {icon}  {title}  —  {pts}"
    line2 = f"  Score total  :  {bar}  {points_after} / 100"

    print()
    print(f"{color}{BOLD}╔{'═' * W}╗{RESET}")
    print(f"{color}{BOLD}║{line1:<{W}}║{RESET}")
    print(f"{color}{BOLD}║{'':^{W}}║{RESET}")
    print(f"{color}{BOLD}║{line2:<{W}}║{RESET}")
    print(f"{color}{BOLD}╚{'═' * W}╝{RESET}")
    print()


def _show_skip_banner():
    """Bannière jaune spéciale pour le skip (debug only)."""
    YELLOW = "\033[93m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

    points = score  # skip ne donne pas de points
    filled = points // 5
    bar = "█" * filled + "░" * (20 - filled)

    W     = 56
    line1 = "  ⚡  EXERCICE SKIPÉ  —  mode debug"
    line2 = f"  Score total  :  {bar}  {points} / 100"

    print()
    print(f"{YELLOW}{BOLD}╔{'═' * W}╗{RESET}")
    print(f"{YELLOW}{BOLD}║{line1:<{W - 1}}║{RESET}")
    print(f"{YELLOW}{BOLD}║{'':^{W}}║{RESET}")
    print(f"{YELLOW}{BOLD}║{line2:<{W}}║{RESET}")
    print(f"{YELLOW}{BOLD}╚{'═' * W}╝{RESET}")
    print()


def _advance():
    global current_level
    current_level += 1
    if current_level >= len(LEVELS):
        print(
            f"\nTous les niveaux complétés !"
            f" Temps : {format_time(elapsed())}"
        )
        sys.exit(0)
    level_name = LEVELS[current_level]
    print(f"\nPassage au niveau {LEVELS[current_level][-1]}…")
    subject = select_subject(level_name)
    if subject:
        print(f"[Niveau {LEVELS[current_level][-1]}] Sujet : {subject.stem}")
        print(f"Sujet copié dans subjects/{subject.name}")
        print("Mets ton rendu dans render/\n")


def _show_solution():
    """Décode et écrit la solution du sujet courant dans subjects/."""
    if current_subject is None:
        return
    level_name = LEVELS[current_level]
    subject_name = current_subject.stem
    level_sols = _SOLUTIONS.get(level_name, {})
    encoded = level_sols.get(subject_name)
    if encoded:
        dest = TRACES_DIR / f"{subject_name}_solution.c"
        dest.write_text(base64.b64decode(encoded).decode())
        print(f"Solution écrite dans traces/{dest.name}")
    else:
        print(f"Pas de solution disponible pour {subject_name}")


# ---------------------------------------------------------------------------
# Timer watcher
# ---------------------------------------------------------------------------

def _timer_watcher():
    global time_expired
    while remaining() > 0:
        time.sleep(1)
    time_expired = True
    print(
        f"\n\n[!] Temps écoulé ! Durée totale : {format_time(elapsed())}\n"
        "Appuie sur Entrée pour quitter."
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _parse_levels(arg: str) -> list[str]:
    """Parse '--levels 3', '--levels 3,4', '--levels 1-3' into level names."""
    all_levels = ["level1", "level2", "level3", "level4"]
    result = []
    for part in arg.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            result += all_levels[int(lo) - 1 : int(hi)]
        else:
            idx = int(part) - 1
            result.append(all_levels[idx])
    return result


def main():
    global start_time, debug_mode, LEVELS

    debug_mode = "--debug" in sys.argv

    if "--levels" in sys.argv:
        idx = sys.argv.index("--levels")
        if idx + 1 < len(sys.argv):
            LEVELS[:] = _parse_levels(sys.argv[idx + 1])

    print("=" * 60)
    print("           EXAM RANK 02 — MOCK EXAM")
    if debug_mode:
        print("               *** MODE DEBUG ***")
    print("=" * 60)
    print(f"Durée       : {format_time(EXAM_DURATION)}")
    print(f"Niveaux     : {chr(44).join(l[-1] for l in LEVELS)}")
    if debug_mode:
        print(
            "Commandes   : "
            "grademe | skip | finish | quit | status | subject"
        )
    else:
        print("Commandes   : grademe | finish | quit | status | subject")
    print("=" * 60)

    start_time = time.time()

    # Nettoyer les dossiers de session
    for d in (RENDER_DIR, SUBJECTS_DIR, TRACES_DIR):
        clear_dir(d)

    # Background timer
    threading.Thread(target=_timer_watcher, daemon=True).start()

    # Pick first subject
    subject = select_subject(LEVELS[current_level])
    if not subject:
        sys.exit(1)
    print(f"\n[Niveau {LEVELS[current_level][-1]}] Sujet : {subject.stem}")
    print(f"Sujet copié dans subjects/{subject.name}")
    print("Mets ton rendu dans render/\n")

    # Main loop
    while True:
        if time_expired:
            print(f"Durée totale : {format_time(elapsed())}")
            sys.exit(0)

        try:
            cmd = _read_line_with_timer().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\nInterrompu. Temps écoulé : {format_time(elapsed())}")
            sys.exit(0)

        if time_expired:
            print(f"Durée totale : {format_time(elapsed())}")
            sys.exit(0)

        if cmd in ("finish", "quit"):
            _show_solution()
            print(f"\nExamen terminé. Temps écoulé : {format_time(elapsed())}")
            sys.exit(0)

        elif cmd == "grademe":
            do_grademe()

        elif cmd == "skip":
            if not debug_mode:
                print(
                    "Commande inconnue : 'skip' "
                    "(disponible uniquement en mode debug)"
                )
            else:
                _show_skip_banner()
                print("[DEBUG] Exercice ignoré.")
                _show_solution()
                _advance()

        elif cmd == "status":
            sub = current_subject.stem if current_subject else '—'
            print(
                f"  Niveau    : {LEVELS[current_level][-1]}/{LEVELS[-1][-1]}\n"
                f"  Sujet     : {sub}\n"
                f"  Écoulé    : {format_time(elapsed())}\n"
                f"  Restant   : {format_time(max(0.0, remaining()))}"
            )

        elif cmd == "subject":
            if current_subject:
                print(f"Sujet actuel : {current_subject.stem}")
                print(f"Fichier      : subjects/{current_subject.name}")
            else:
                print("Aucun sujet sélectionné.")

        elif cmd == "":
            pass

        else:
            print(f"Commande inconnue : '{cmd}'")
            if debug_mode:
                print(
                    "Commandes : grademe | skip | finish"
                    " | quit | status | subject"
                )
            else:
                print(
                    "Commandes : grademe | finish"
                    " | quit | status | subject"
                )


if __name__ == "__main__":
    main()
