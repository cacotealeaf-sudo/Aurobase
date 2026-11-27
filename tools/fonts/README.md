# 網站字型來源檔

`ZevHeiTC-F-VF.woff2` 是宙黑體 F 版（Zev Hei TC，保留底腳）的完整字集，
已從原始可變字型固定為 wdth 100、IDSP 0，只保留 wght 300–900 一軸（約 10 MB）。

- `tools/build-font-subset.sh` 從這支切出 `WOFF2/ZevHeiTC-F.subset.woff2`（只含站上用字）。
- `tools/build-og-images.py` 與 `tools/guides/fsc_checklist.py` 直接讀這支畫圖、出 PDF。
- 這個資料夾不發布到 GitHub Pages（`_config.yml` 排除 `tools/`）。

原始檔：https://github.com/chiron-fonts/zev-hei-tc（`VAR_OTF/ZevHeiTC-F-VF.otf`，v0.008）
授權：SIL OFL 1.1，見 `ZevHeiTC-OFL.txt`（`WOFF2/` 內也放一份，跟著子集一起發布）。

重做這支（約 7 分鐘；先 subset 再 instance，反過來 fontTools 會在 CFF2 的 VarStore 出錯）：

```python
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
import io
o = subset.Options(); o.layout_features = ['*']; o.hinting = False; o.notdef_outline = True
o.name_IDs = ['*']; o.name_languages = ['*']
f = TTFont('ZevHeiTC-F-VF.otf'); s = subset.Subsetter(o); s.populate(unicodes=f.getBestCmap().keys()); s.subset(f)
b = io.BytesIO(); f.save(b); b.seek(0)
g = instancer.instantiateVariableFont(TTFont(b), {'wdth': 100, 'IDSP': 0, 'wght': (300, 900)})
del g['BASE']   # instancer 不處理 BASE 的 VarStore，留著會讓之後的 pyftsubset 存檔失敗
g.flavor = 'woff2'; g.save('tools/fonts/ZevHeiTC-F-VF.woff2')
```
