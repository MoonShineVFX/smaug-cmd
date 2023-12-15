from smaug_cmd.domain import parsing as ps


def smaug_resource_uploader(md_filepath):
    """Upload a asset from resource team to smaug.

    :param base_dir: The base directory of the resource.
    :return: The resource id.
    """
    # 分類的部份，從 MD 檔來產生
    

    res_folder_type = ps.which_kind_resource(base_dir)
    # 找出對應的 resource folder type, 才能收集資料

    collect_process = ps.resource_handler_mapping[res_folder_type]

    asset_template = collect_process(base_dir)

    create_asset_via_template(asset_template)

