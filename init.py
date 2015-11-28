def init(app):
    import taciturn.hooks
    import taciturn.core
    app.register_blueprint(taciturn.core.core_bp)
    app.register_blueprint(taciturn.hooks.hooks_bp)
