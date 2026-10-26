| transformation | C2PA verdict | watermark detected (mean bit acc.) | fingerprint match (mean dist.) |
|---|---|---|---|
| ORIGINAL (as issued) | Trusted x3 | 3/3 (1.0) | 3/3 (0.0/256) |
| none (file copy) | Trusted x3 | 3/3 (1.0) | 3/3 (0.0/256) |
| 1 byte changed | Invalid x3 | 3/3 (1.0) | 3/3 (9.7/256) |
| re-save as PNG (strip metadata) | NoManifest x3 | 3/3 (1.0) | 3/3 (0.0/256) |
| JPEG q85 | NoManifest x3 | 3/3 (0.969) | 3/3 (0.3/256) |
| JPEG q60 | NoManifest x3 | 3/3 (0.885) | 3/3 (1.3/256) |
| messenger-like (1280px, q70) | NoManifest x3 | 3/3 (0.912) | 3/3 (1.3/256) |
| resize 50% | NoManifest x3 | 0/3 (0.474) | 3/3 (0.7/256) |
| gaussian noise s=8 | NoManifest x3 | 3/3 (1.0) | 3/3 (5.0/256) |
| crop 80% center | NoManifest x3 | 0/3 (0.5) | 0/3 (94.0/256) |
| rotate 5 deg | NoManifest x3 | 0/3 (0.531) | 0/3 (55.7/256) |
| mirror | NoManifest x3 | 0/3 (0.5) | 0/3 (142.3/256) |
| browser screenshot 1:1 (headless Chrome) | NoManifest x3 | 3/3 (1.0) | 3/3 (0.0/256) |
| browser screenshot, 125% scaling + page border | NoManifest x3 | 0/3 (0.531) | 0/3 (49.7/256) |
| C2PA-aware crop + re-sign | Trusted x3 | 0/3 (0.5) | 0/3 (94.0/256) |
