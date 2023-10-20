from smaug_cmd.domain import command as cmd
from smaug_cmd.adapter.cmd_handlers import asset, representation as resp, zip


handle_map = {
    cmd.CreateAsset: asset.create_asset,
    cmd.CreateRepresentation: resp.create_representation,
    cmd.UploadRepresentation: resp.upload_representation,
    cmd.CreateZip: zip.create_zip
}


def handler(payload):
    handler_func = handle_map[type(payload)]
    return handler_func(payload)