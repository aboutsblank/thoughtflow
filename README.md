# thoughtflow

Tools to help me with the human-computer interaction.

## Specification

### Scope

- local scope `$(getcwd)/.thoughtflow/..`
- global scope `$HOME/.thoughtflow/..`

### Categories

- DAILY
- FEATURE
- IDEA
- PROBLEM
- TASK

### Use cases

```bash
<category> [OPTIONS] (STDIN|micro|<text>)
```

#### `idea`

```
# should save "Quick Idea" to respective scope
idea (-l|-g) "Quick Idea"

# should open preferred text editor and on save / quit append the input to respective scope
idea (-l|-g)
```

#### `problem`

```
# -p | --project
problem -p="THESIS" "Bug bzgl Laden der Daten"
```

#### `daily`

```bash

# opens the current daily note ($VAULT/<YYYY-MM-DD>.md)
daily

# opens the specified daily note ($VAULT/<YYYY-MM-DD>.md)
daily <YYYY-MM-DD>
daily (yesterday|today|tomorrow)
daily (-i|0|+i)

alias dy=daily

```

## Dev Guide

### Build Application

### Project Structure

/sandbox/ 
use this directory as a virtual sandbox so always test out file changes there
not in the current dir
so always start the application from there
start the software as an independent user


### CI/CD

- Linter
- Formatter
- Typechecker
- Tests
- backend(db): migration and schema file match
