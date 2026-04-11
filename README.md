# IB Computer Science Internal Assessment

This is the repo for my IB Computer Science Internal Assessment. It contains the code for my project, as well as any relevant documentation and resources.

## Important Note

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
Note: run this command from the root of the repository, not from within the submodule directory.

Or, you can navigate to the submodule directory and pull the latest changes:

```bash
cd ib-cs-ia-guide
git pull origin main
```