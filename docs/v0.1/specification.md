\# FireSohouAI Version 0.1 Specification



Version: 0.1.0  

Status: Draft  

Author: FireSohouAI Project  

Last Updated: 2026-06-26



\---



\# 1. Purpose



FireSohouAI is an open-source project that uses AI technologies to support firefighting drill training.



Version 0.1 aims to establish the first end-to-end workflow:



1\. Record a training session.

2\. Analyze body movements.

3\. Detect firefighting equipment.

4\. Produce analysis videos and CSV files.

5\. Generate a simple analysis report.



This version is a prototype intended for training support rather than official competition judging.



\---



\# 2. Scope



The following functions are included in Version 0.1.



| Item | Description |

|------|-------------|

| Drill | Portable Pump Drill |

| Camera | Single fixed camera |

| Resolution | 1920×1080 (1080p) |

| Frame Rate | 30 fps |

| Analysis | Offline |

| Platform | Windows PC |

| Recording | Raspberry Pi Camera or USB Camera |

| Pose Estimation | MediaPipe |

| Object Detection | YOLO |

| Report | CSV + Markdown |



\---



\# 3. Objectives



The project shall:



\- Record drill videos.

\- Estimate firefighter body posture.

\- Detect basic firefighting equipment.

\- Export numerical data.

\- Visualize analysis results.

\- Build a reusable AI analysis pipeline.



\---



\# 4. Out of Scope



Version 0.1 does NOT include:



\- Official scoring

\- Automatic judging

\- Real-time inference

\- Four-person simultaneous tracking

\- Cloud services

\- Smartphone synchronization

\- Raspberry Pi AI inference

\- Large-scale datasets



These items are planned for future releases.



\---



\# 5. Input Specification



\## Video



| Item | Value |

|------|-------|

| Format | MP4 |

| Codec | H.264 |

| Resolution | 1920×1080 |

| FPS | 30 |

| Camera | Fixed |



Recommended recording distance:



\- 15–25 meters

\- Entire firefighter visible

\- Minimal camera movement



\---



\# 6. Output Specification



Version 0.1 produces:



```

evaluation/output/



├── pose\_overlay.mp4

├── yolo\_overlay.mp4

├── combined\_analysis.mp4

├── pose\_angles.csv

├── object\_detection.csv

├── analysis\_summary.csv

└── analysis\_report.md

```



\---



\# 7. Pose Analysis



MediaPipe estimates:



\- Left elbow

\- Right elbow

\- Left knee

\- Right knee

\- Left hip

\- Right hip

\- Trunk angle



Each frame stores:



\- Frame number

\- Timestamp

\- Joint angles



Example:



| Frame | Time | Left Knee |

|-------|------|-----------|

| 150 | 5.000 | 138.5° |



\---



\# 8. Object Detection



Initial YOLO classes:



| Class |

|------|

| person |

| hose |



Optional:



\- nozzle

\- portable\_pump



Detection results include:



\- Confidence

\- Bounding box

\- Timestamp



\---



\# 9. Event Detection



Version 0.1 attempts to estimate:



\- Motion Start

\- Running Start

\- Hose Pickup



Future versions will include:



\- Water Start

\- Coupling Complete

\- Target Knockdown



\---



\# 10. Folder Structure



```

FireSohouAI/



docs/

mediapipe/

yolo/

raspberry\_pi/

evaluation/

datasets/

sample\_data/

sora/

```



\---



\# 11. Software Stack



| Software | Purpose |

|-----------|---------|

| Python | Main language |

| OpenCV | Video processing |

| MediaPipe | Pose estimation |

| YOLO | Object detection |

| Pandas | CSV |

| NumPy | Numerical computation |



\---



\# 12. Raspberry Pi



Initial recording platform:



\- Raspberry Pi 5

\- Raspberry Pi Camera

\- USB SSD



Responsibilities:



\- Record videos

\- Save files

\- Transfer to Windows PC



No AI inference is required on Raspberry Pi in Version 0.1.



\---



\# 13. Sora



Sora is used for:



\- Educational videos

\- Storyboards

\- Ideal movement visualization



Sora output is reference material only and does not replace official firefighting manuals.



\---



\# 14. Completion Criteria



Version 0.1 is considered complete when:



\- Training video can be recorded.

\- MediaPipe analysis succeeds.

\- Joint angles are exported.

\- YOLO detects at least person and hose.

\- Combined analysis video is generated.

\- CSV files are exported.

\- Markdown report is generated.



\---



\# 15. Future Versions



\## Version 0.2



\- Multiple firefighters

\- More equipment classes

\- Improved event detection



\## Version 0.3



\- Semi-automatic scoring

\- Drill comparison

\- Trend analysis



\## Version 1.0



\- Practical training support system

\- Multi-camera support

\- Competition-ready analysis



\---



\# 16. License



Apache License 2.0



\---



\# 17. Project Philosophy



FireSohouAI is an educational open-source project.



Its mission is to improve firefighting training through modern AI technologies while respecting official firefighting manuals and safety practices.



The project values:



\- Education

\- Transparency

\- Reproducibility

\- Open collaboration

\- Continuous improvement

