# Facial Shapekeys+

A fork of [Shape Keys+](https://github.com/MichaelGlenMontague/shape_keys_plus) with a big focus on improving the automatization and workflow on Face Tracking blendshapes (ARKit and UE)

Add-on made for [Blender](https://www.blender.org/) which adds a panel containing extra features for creating, sorting, viewing, and driving shape keys.

Automatically hides the default ***Shape Keys*** panel, which can be enabled again via the add-on's preferences. 


## The rest here hasn't been updated and contains the Shapekeys+ readme. It'll be updated eventually
***Shape Keys+*** was made to help with managing hundreds of shape keys on a fully rigged character. It focuses on saving time and decreasing the number of clicks needed for common operations such as moving or copying shape keys.

Click-holding or click-dragging on one of the **Add** / **Copy** / **Remove** sidebar buttons will open its respective specials menu, containing extra operations related to the respective button.

![0|369x821](./screenshot.png)
> Screenshot taken in Blender 2.83.

# Features

- **Folders**
> Manage shape keys with folders.

- **Shape Key Placement**
> Control where shape keys are automatically placed after specific operations.

- **Copy Shape Key**
> Copy the shape key, its driver, and all or some of its properties. Capable of copying and mirroring at the same time. Mirrored copies automatically detect and rename Left/Right (and similar) naming conventions using Blender's own name-flipping logic.

- **Copy Shape Key, Inverted**
> Duplicate a shape key and invert it relative to its relative key - equivalent to blending it to -1 and baking the result into a new shape key.

- **ARKit / Unified Expressions Automation**
> Automatically generate all 52 empty ARKit blend shapes, or the full Unified Expressions Base/Blended shape set, each parented into auto-created "---Face Tracking---" (and, for Unified Expressions, a nested "---Blended Shapes---") folder.

- **Multi-Selection**
> Perform basic operations on multiple shape keys and folders at once. Compatible with “New Combined” as it creates a new shape out of a mix of the selected shape keys, even if some of them currently have a value of 0. Features compatible with multi-selection become exposed when at least one shape key or folder is selected.

- **Driver Sub-Panel**
> View and edit the driver for a shape key’s value directly within the Shape Keys+ panel.

- **Manual Translation**
> All UI elements are set up for manual translation, with the two current languages being English and Japanese. The language can be configured at any time simply by changing the language property in the shape_keys_plus/config.ini file and restarting Blender.

---
# Credits
[MichaelGlenMontague](https://github.com/MichaelGlenMontague) - Original work on [Shapekeys+](https://github.com/MichaelGlenMontague/shape_keys_plus) from which this project is based on
