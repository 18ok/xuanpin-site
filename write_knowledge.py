import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"D:\u7389\u4ed3\u7cfb\u7edf\u5f55\temu\u7cfb\u7edf\u9884\u00b7\u521b\u9879\u76ee\玄\u54c1\u5fc3\u51b3\思\u7ef4\u8fed\u4ee3\知\u8bc6\u7d22\u5f15\u5206\u6790-20260608.md"

content = """---
title: """玄\u54c1\u5fc3\u51b3 \u00b7 \u77e5\u8bc6\u7d22\u5f15\u6a21\u5757\u5206\u6790"""
type: strategy
date: 2026-06-08
author: Codex（商\u4e1a\u5408\u4f19\u4eba\u89c6\u89d2）
status: 待\u7389\u6210\u5ba1\u9605
---"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: " + str(len(content)) + " bytes")
