# flow: 

main.registry.addDefaultRegistry()
main.repository.addInitialRepository()
main.extensions.loadInstalled()
    main.extensions.checkForAllUpdates()
    if needed:
        main.extensions.updateAll()
main.ui.start()

# TODO:
[ ] recommendations = what are they?
[ ] Logic as classes - define
[ ] 