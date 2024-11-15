# Iterative Transformation

This Inkscape extension duplicates selected objects with incremental transformations. Users can adjust scaling, rotation, translation, and skew parameters, and choose whether to scale the stroke width alongside the object.

<img src="example.svg" alt="Example" width="800">

## Parameters

- **Transformation Center**: The reference point for transformations (e.g., center, top-left).
- **Rotation Center**: Rotate aroud the transformation center of the duplicate or the original object (e.g., to create spirals).
- **Scale**: Scaling factor for each iteration (e.g., 1.1 for a 10% increase).
- **Rotate**: Rotation angle in degrees.
- **Translate X / Y**: Translation offsets along X and Y axes.
- **Skew X / Y**: Skew angles along the X and Y axes.
- **Iterations**: Number of duplicates created.
- **Scale Stroke Width**: Option to scale the stroke width with object scaling.

## Usage

1. Install this extension in your Inkscape extensions folder.
2. Restart Inkscape.
3. Open your document and select the objects you want to duplicate and transform.
4. Go to `Extensions > Generate from Path > Iterative Transformation`.
5. Configure the parameters and click **Apply**.

## License

This extension is licensed under the MIT License.
