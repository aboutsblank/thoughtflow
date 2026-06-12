import cli

if __name__ == "__main__":

    settings, element = cli.initApp()

    path = cli.getLocalPath()

    if settings.scope == cli.Scope.GLOBAL:
        path = cli.getGlobalPath()

    path = path / ".{}".format(cli.APP_NAME)
    if not cli.Path.exists(path):
        cli.os.mkdir(path)

    path = path / "{}".format(settings.usecase)

    # test if exists and writable
    # if yes open in append mode otherwise error
    with path.open(mode="a+") as file:
        serialized = cli.serialize(element)
        file.write("{}\n".format(serialized))