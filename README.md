# IB Computer Science Internal Assessment

**Assignment Management and Tracking System**

This is the repo for my IB Computer Science Internal Assessment. It contains the code for my project, as well as any relevant documentation and resources.

- the proposal is located in [Proposal.md](Proposal.md)
- the success criteria is located in [Success Criteria.md](Success%20Criteria.md).
- the plan is located in [Plan.md](Plan.md)

## UML

This project uses [Mermaid](https://mermaid.js.org/) (.mmd) class diagrams as the source of truth for diagram *content*, which is rendered, styled, and exported using [draw.io](https://www.drawio.com/).

Roles of files in `docs/UML/<name>/`:

| file | role |
| --- | --- |
| `*.mmd` | Mermaid class diagram code (source) |
| `*.drawio` | styled and arranged diagram |
| `*.svg`, `*.png` | exported images |

A `.drawio` file is created once by importing the `.mmd` (**Arrange → Insert → Advanced → Mermaid**), then styled and arranged by hand. Re-importing regenerates the shapes and discards that layout, so the `.drawio` must be edited directly instead.

The `~tools` directory contains scripts and other tools to help with diagram management.

### Building

Exports use the draw.io desktop CLI, which can be installed using:

```bash
winget install JGraph.Draw
```

**Note:** This installs to `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe` and is not added to `PATH`, so the folder must be added to `PATH` or the binary must be called by full path.

Then, the following command can be used to export the diagrams to svg and png:

```bash
cd .\docs\UML\ ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f svg --theme light -o Core/CoreUML.svg Core/CoreUML.drawio ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f png -s 1 --theme light -o Core/CoreUML.png Core/CoreUML.drawio ;
cd .\docs\UML\ ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f svg --theme light -o ADT/ADTUML.svg ADT/ADTUML.drawio ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f png -s 1 --theme light -o ADT/ADTUML.png ADT/ADTUML.drawio
cd .\docs\ERD\ ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f svg --theme light -o docs/ERD/ERD.svg docs/ERD/ERD.drawio ; & "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" -x -f png -s 1 --theme light -o docs/ERD/ERD.png docs/ERD/ERD.drawio

```

## Submodule

This project uses a submodule which contains templates and other resources. To clone this repository with the submodule, use the following command:

```bash
git clone --recurse-submodules https://github.com/sukarth/ib-cs-ia.git
```

If you have already cloned the repository without the submodule, you can initialize and update the submodule with the following commands:

```bash
git submodule update --init --recursive
```

To simply sync/pull the latest changes from the submodule, use:

```bash
git submodule update --remote --merge --recursive
```
   - Note: run this command from the root of the repository, not from within the submodule directory.

Or, you can navigate to the submodule directory and pull the latest changes:

```bash
cd ib-cs-ia-guide
git pull origin main
```