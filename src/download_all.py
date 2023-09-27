import biomodels
import pooch
from tqdm.contrib.concurrent import thread_map

# Ignore warning logs
pooch.get_logger().setLevel("WARNING")


def download(model: str):
    try:
        biomodels.get_omex(model)
    except Exception:
        return model


if __name__ == "__main__":
    models = biomodels.get_all_identifiers()
    missing = len(thread_map(download, models))
    print(missing)
