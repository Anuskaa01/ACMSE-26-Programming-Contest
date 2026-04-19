from collections import deque
from pathlib import Path
import csv

import numpy as np
from PIL import Image


THRESHOLD = 15


def segment_image(pixels: np.ndarray, threshold: int = THRESHOLD) -> tuple[np.ndarray, int]:
	"""BFS labeling with 4-neighbor connectivity and intensity threshold."""
	if pixels.ndim != 2:
		raise ValueError("Expected a 2D grayscale image array.")

	h, w = pixels.shape
	labels = np.full((h, w), -1, dtype=np.int32)
	segment_id = 0
	q: deque[tuple[int, int]] = deque()

	for r in range(h):
		for c in range(w):
			if labels[r, c] != -1:
				continue

			segment_id += 1
			labels[r, c] = segment_id
			q.append((r, c))

			while q:
				cr, cc = q.popleft()
				center = int(pixels[cr, cc])

				if cr > 0:
					nr, nc = cr - 1, cc
					if labels[nr, nc] == -1 and abs(center - int(pixels[nr, nc])) <= threshold:
						labels[nr, nc] = segment_id
						q.append((nr, nc))

				if cr + 1 < h:
					nr, nc = cr + 1, cc
					if labels[nr, nc] == -1 and abs(center - int(pixels[nr, nc])) <= threshold:
						labels[nr, nc] = segment_id
						q.append((nr, nc))

				if cc > 0:
					nr, nc = cr, cc - 1
					if labels[nr, nc] == -1 and abs(center - int(pixels[nr, nc])) <= threshold:
						labels[nr, nc] = segment_id
						q.append((nr, nc))

				if cc + 1 < w:
					nr, nc = cr, cc + 1
					if labels[nr, nc] == -1 and abs(center - int(pixels[nr, nc])) <= threshold:
						labels[nr, nc] = segment_id
						q.append((nr, nc))

	return labels, segment_id


def save_label_image(labels: np.ndarray, out_path: Path) -> None:
	"""Save labels to PNG using a dtype that can hold the largest segment id."""
	max_id = int(labels.max())

	if max_id <= 255:
		img = Image.fromarray(labels.astype(np.uint8))
	elif max_id <= 65535:
		img = Image.fromarray(labels.astype(np.uint16))
	else:
		img = Image.fromarray(labels.astype(np.int32))

	img.save(out_path)


def process_folder(images_dir: Path, output_dir: Path) -> list[tuple[str, int, int, int]]:
	"""Run segmentation on all PNGs in one folder."""
	rows: list[tuple[str, int, int, int]] = []
	output_dir.mkdir(parents=True, exist_ok=True)

	for image_path in sorted(images_dir.glob("*.png")):
		with Image.open(image_path) as img:
			gray = img.convert("L")
			pixels = np.array(gray, dtype=np.uint8)

		labels, num_segments = segment_image(pixels, threshold=THRESHOLD)
		save_label_image(labels, output_dir / image_path.name)

		h, w = pixels.shape
		rows.append((str(image_path), h, w, num_segments))
		print(f"Processed {image_path.name}: {num_segments} segments")

	return rows


def write_summary(rows: list[tuple[str, int, int, int]], summary_path: Path) -> None:
	summary_path.parent.mkdir(parents=True, exist_ok=True)
	with summary_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["image_path", "height", "width", "num_segments"])
		writer.writerows(rows)


def main() -> None:
	root = Path(__file__).resolve().parent

	dataset_dirs = [
		(root / "train" / "images", root / "outputs" / "train"),
		(root / "test" / "images", root / "outputs" / "test"),
	]

	all_rows: list[tuple[str, int, int, int]] = []
	for images_dir, output_dir in dataset_dirs:
		if not images_dir.exists():
			continue
		all_rows.extend(process_folder(images_dir, output_dir))

	write_summary(all_rows, root / "outputs" / "summary.csv")
	print(f"Done. Processed {len(all_rows)} images.")


if __name__ == "__main__":
	main()