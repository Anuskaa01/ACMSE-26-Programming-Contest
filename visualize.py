from pathlib import Path

import numpy as np
from PIL import Image


def build_color_lut(max_id: int) -> np.ndarray:
	"""Deterministic color table so the same segment id always gets the same color."""
	lut = np.zeros((max_id + 1, 3), dtype=np.uint8)
	ids = np.arange(max_id + 1, dtype=np.int64)

	# Keep colors bright and varied for easier presentation.
	lut[:, 0] = ((ids * 37) % 200 + 30).astype(np.uint8)
	lut[:, 1] = ((ids * 67) % 200 + 30).astype(np.uint8)
	lut[:, 2] = ((ids * 97) % 200 + 30).astype(np.uint8)
	lut[0] = (0, 0, 0)
	return lut


def colorize_labels(label_img: np.ndarray) -> np.ndarray:
	labels = label_img.astype(np.int64, copy=False)
	max_id = int(labels.max())
	lut = build_color_lut(max_id)
	return lut[labels]


def to_rgb_gray(img_gray: np.ndarray) -> np.ndarray:
	return np.repeat(img_gray[:, :, None], 3, axis=2)


def make_side_by_side(gray: np.ndarray, colorized: np.ndarray) -> np.ndarray:
	separator = np.full((gray.shape[0], 6, 3), 255, dtype=np.uint8)
	left = to_rgb_gray(gray)
	return np.concatenate([left, separator, colorized], axis=1)


def visualize_split(root: Path, split: str) -> int:
	image_dir = root / split / "images"
	label_dir = root / "outputs" / split
	out_dir = root / "visualizations" / split
	out_dir.mkdir(parents=True, exist_ok=True)

	count = 0
	for image_path in sorted(image_dir.glob("*.png")):
		label_path = label_dir / image_path.name
		if not label_path.exists():
			continue

		with Image.open(image_path) as img:
			gray = np.array(img.convert("L"), dtype=np.uint8)

		with Image.open(label_path) as lab:
			labels = np.array(lab)

		colorized = colorize_labels(labels)
		preview = make_side_by_side(gray, colorized)
		Image.fromarray(preview).save(out_dir / image_path.name)
		count += 1

	print(f"{split}: created {count} visualizations")
	return count


def main() -> None:
	root = Path(__file__).resolve().parent
	train_count = visualize_split(root, "train")
	test_count = visualize_split(root, "test")
	print(f"Done. Total visualizations: {train_count + test_count}")


if __name__ == "__main__":
	main()