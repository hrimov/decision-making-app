import aioboto3


class AIOBotoGateway:
    """
    Generic AIOBoto3 gateway that requires an initialized session (with access-secret keys)
    """

    def __init__(self, session: aioboto3.Session):
        self.session = session
