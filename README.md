# CompetitionManager

Small web application for managing archery competitions, up to this point it's in an development state.

## Tech stack

The Backend is completely written in Python 3.7 using the Flask micro framework.
The Frontend uses jQuery and Materialize.
This Repository is an PyCharm Project, which means you can continue developing it pretty easily.

## Docker

### Build

```
./scripts/container-build.sh
```

### Run

```
ENGINE=podman
$ENGINE run --rm -it -p 8080:9000 -v $PWD/Database:/app/Database chevdor/archery-competition-manager
```
