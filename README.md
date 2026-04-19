# ACMSE 2026 Undergraduate Programming Contest: Image Segmentation

## Project Overview
This project is part of the ACMSE 2026 Programming Contest. The goal is to implement an image segmentation algorithm that partitions grayscale images into distinct regions based on pixel intensity similarity.

## The Challenge
Participants must develop a solution that assigns every pixel in a grayscale image to a **Segment ID** based on local connectivity and a fixed intensity threshold.

This problem emphasizes algorithm design, correctness, and efficiency.

---

## Dataset Structure

The dataset is provided in the 'contest_dataset/' directory:

- 'images/': Grayscale PNG images for segmentation

Each image should be processed independently.

---

## Segmentation Rules & Constraints

All submissions must strictly follow these rules:

1. **4-Directional Adjacency**  
   Only consider neighbors in four directions:
   up, down, left, right  
   (diagonal connections are NOT allowed)

2. **Intensity Threshold**  
   Two adjacent pixels belong to the same segment if:
   
   |I(P1) - I(P2)| ≤ 15

3. **Unique Assignment**  
   Every pixel must belong to exactly one segment

---

## Output Requirements

For each input image, your program must generate:

1. A segmentation result saved as an image (PNG), where:
   - Each pixel value represents a Segment ID  
   - Output image has the same dimensions as input  

2. A summary file (optional) containing:
   - Total number of segments per image  

---

## Submission Requirements

Your GitHub repository must include:

1. **Source Code**
   - Well-organized and documented
   - Reproducible results

2. **Output Results**
   - A folder containing segmentation outputs for all images  
   - Filenames must match the input images exactly  

3. **Project Description**
   - Description of your approach  
   - Algorithm used (e.g., BFS, DFS, Union-Find)  
   - Any optimizations  

4. **Demo Video (3–5 minutes)**
   - Brief explanation of your solution  

---

## Restrictions

- **No External AI APIs**
  (e.g., OpenAI, Gemini, etc.)

- **No Pre-built Segmentation Functions**
  (e.g., OpenCV watershed, skimage.segmentation)

- **Allowed Libraries**
  - NumPy  
  - PIL / Pillow  
  - Standard Python libraries  

---

## Evaluation Criteria

- **Correctness (40%)**
  - Proper application of segmentation rules  

- **Consistency (20%)**
  - Uniform logic across all images  

- **Efficiency (20%)**
  - Runtime performance  

- **Code Quality (20%)**
  - Readability, structure, and documentation  

---

## Notes

- Multiple correct solutions may exist  
- Segment IDs do not need to match a specific numbering scheme  
- Focus on correctness and clarity of implementation  

---

Good luck, and we look forward to your solutions!

---

## Implementation in this Repository

We implemented segmentation in `segment.py` using BFS connected components.

1. Load each input image as grayscale
2. Scan every pixel and start a BFS on unvisited pixels
3. Grow the component in 4 directions only
4. Add a neighbor only if the intensity rule holds:
   - |I(P1) - I(P2)| <= 15
5. Save a label image with the same filename as the input

### Efficiency

- Time complexity: O(H x W) per image
- Space complexity: O(H x W)

### Run

From the project root:

```bash
python segment.py
```

### Generated outputs

- `outputs/train/`: segmentation results for all images in `train/images/`
- `outputs/test/`: segmentation results for all images in `test/images/`
- `outputs/summary.csv`: per-image segment counts

### Optional demo visualizations

To generate side-by-side previews (original grayscale | colorized segments):

```bash
python visualize.py
```

Generated files:

- `visualizations/train/`
- `visualizations/test/`