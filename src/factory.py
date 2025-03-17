from fastapi import FastAPI
from pydantic import BaseModel

import controller
import datastore
import interactor
import router


def newApp() -> FastAPI:
    """FastAPIの初期化とDIを一元管理する"""

    app = FastAPI()

    # Repository（Datastore）の作成
    rg = datastore.RowDataGetter()
    
    # UseCase（Interactor）の作成
    df = interactor.DataFormatter(rg=rg)
    qe = interactor.QuaternionEstimator()
    de = interactor.DistanceEstimator()
    mc = interactor.MultipartCreator()
    cc = interactor.CsvCreator()
    zc = interactor.ZipCreator()
    # Controller の作成
    ec = controller.EstimationController(
        df=df,
        qe=qe,
        de=de,
        cc=cc,
        zc=zc,
        mc=mc
    )

	# app.state に EstimationController をセット
    app.state.ec = ec
    # ルートを登録
    router.registerRoutes(app)

    return app
