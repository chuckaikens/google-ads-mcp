"""Tools for mutating Google Ads resources (ads, campaigns, ad groups, keywords)."""

from typing import Optional
from ads_mcp.coordinator import mcp
import ads_mcp.utils as utils
import json


@mcp.tool()
def update_ad_url(
    customer_id: str,
    ad_id: str,
    final_url: str,
) -> dict:
    """Update the final URL on an ad.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_id: The ad ID to update
        final_url: The new final URL for the ad
    """
    client = utils.get_googleads_client()
    ad_service = client.get_service("AdService")

    ad_operation = client.get_type("AdOperation")
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(customer_id, ad_id)
    ad.final_urls.append(final_url)

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("final_urls")
    ad_operation.update_mask.CopyFrom(field_mask)

    response = ad_service.mutate_ads(
        customer_id=customer_id,
        operations=[ad_operation],
    )

    return {
        "status": "success",
        "updated_ad": response.results[0].resource_name,
        "new_final_url": final_url,
    }


@mcp.tool()
def update_ad_status(
    customer_id: str,
    ad_group_id: str,
    ad_id: str,
    status: str,
) -> dict:
    """Update the status of an ad (enable, pause, or remove).

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the ad
        ad_id: The ad ID to update
        status: The new status: ENABLED, PAUSED, or REMOVED
    """
    client = utils.get_googleads_client()
    ad_group_ad_service = client.get_service("AdGroupAdService")

    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.update
    ad_group_ad.resource_name = ad_group_ad_service.ad_group_ad_path(
        customer_id, ad_group_id, ad_id
    )

    status_enum = client.enums.AdGroupAdStatusEnum
    ad_group_ad.status = getattr(status_enum, status.upper())

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("status")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_ad": response.results[0].resource_name,
        "new_status": status.upper(),
    }


@mcp.tool()
def update_campaign_status(
    customer_id: str,
    campaign_id: str,
    status: str,
) -> dict:
    """Update the status of a campaign (enable or pause).

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        campaign_id: The campaign ID to update
        status: The new status: ENABLED or PAUSED
    """
    client = utils.get_googleads_client()
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    status_enum = client.enums.CampaignStatusEnum
    campaign.status = getattr(status_enum, status.upper())

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("status")
    operation.update_mask.CopyFrom(field_mask)

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_campaign": response.results[0].resource_name,
        "new_status": status.upper(),
    }


@mcp.tool()
def update_ad_group_status(
    customer_id: str,
    ad_group_id: str,
    status: str,
) -> dict:
    """Update the status of an ad group (enable or pause).

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to update
        status: The new status: ENABLED or PAUSED
    """
    client = utils.get_googleads_client()
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )

    status_enum = client.enums.AdGroupStatusEnum
    ad_group.status = getattr(status_enum, status.upper())

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("status")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_ad_group": response.results[0].resource_name,
        "new_status": status.upper(),
    }


@mcp.tool()
def update_keyword_url(
    customer_id: str,
    ad_group_id: str,
    criterion_id: str,
    final_url: str,
) -> dict:
    """Update the final URL on a keyword criterion.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the keyword
        criterion_id: The keyword criterion ID to update
        final_url: The new final URL for the keyword
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.update
    criterion.resource_name = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )
    criterion.final_urls.append(final_url)

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("final_urls")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_keyword": response.results[0].resource_name,
        "new_final_url": final_url,
    }


@mcp.tool()
def update_keyword_status(
    customer_id: str,
    ad_group_id: str,
    criterion_id: str,
    status: str,
) -> dict:
    """Update the status of a keyword (enable, pause, or remove).

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the keyword
        criterion_id: The keyword criterion ID to update
        status: The new status: ENABLED, PAUSED, or REMOVED
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.update
    criterion.resource_name = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )

    status_enum = client.enums.AdGroupCriterionStatusEnum
    criterion.status = getattr(status_enum, status.upper())

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("status")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_keyword": response.results[0].resource_name,
        "new_status": status.upper(),
    }


@mcp.tool()
def add_keyword(
    customer_id: str,
    ad_group_id: str,
    keyword_text: str,
    match_type: str,
    final_url: Optional[str] = None,
    cpc_bid_micros: Optional[int] = None,
) -> dict:
    """Add a new keyword to an ad group.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to add the keyword to
        keyword_text: The keyword text
        match_type: The match type: EXACT, PHRASE, or BROAD
        final_url: Optional final URL override for this keyword
        cpc_bid_micros: Optional CPC bid in micros (e.g., 1500000 = $1.50)
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create
    criterion.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    criterion.keyword.text = keyword_text
    criterion.keyword.match_type = getattr(
        client.enums.KeywordMatchTypeEnum, match_type.upper()
    )

    if final_url:
        criterion.final_urls.append(final_url)

    if cpc_bid_micros:
        criterion.cpc_bid_micros = cpc_bid_micros

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "created_keyword": response.results[0].resource_name,
        "keyword_text": keyword_text,
        "match_type": match_type.upper(),
    }


@mcp.tool()
def remove_keyword(
    customer_id: str,
    ad_group_id: str,
    criterion_id: str,
) -> dict:
    """Remove a keyword from an ad group (permanent delete).

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the keyword
        criterion_id: The keyword criterion ID to remove
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    operation.remove = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "removed_keyword": response.results[0].resource_name,
    }


@mcp.tool()
def add_negative_keyword(
    customer_id: str,
    ad_group_id: str,
    keyword_text: str,
    match_type: str,
) -> dict:
    """Add a negative keyword to an ad group to block unwanted traffic.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to add the negative keyword to
        keyword_text: The negative keyword text
        match_type: The match type: EXACT, PHRASE, or BROAD
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create
    criterion.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    criterion.negative = True
    criterion.keyword.text = keyword_text
    criterion.keyword.match_type = getattr(
        client.enums.KeywordMatchTypeEnum, match_type.upper()
    )

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "created_negative_keyword": response.results[0].resource_name,
        "keyword_text": keyword_text,
        "match_type": match_type.upper(),
    }


@mcp.tool()
def add_campaign_negative_keyword(
    customer_id: str,
    campaign_id: str,
    keyword_text: str,
    match_type: str,
) -> dict:
    """Add a negative keyword at the campaign level to block unwanted traffic across all ad groups.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        campaign_id: The campaign ID to add the negative keyword to
        keyword_text: The negative keyword text
        match_type: The match type: EXACT, PHRASE, or BROAD
    """
    client = utils.get_googleads_client()
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignCriterionOperation")
    criterion = operation.create
    criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    criterion.negative = True
    criterion.keyword.text = keyword_text
    criterion.keyword.match_type = getattr(
        client.enums.KeywordMatchTypeEnum, match_type.upper()
    )

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "created_campaign_negative": response.results[0].resource_name,
        "keyword_text": keyword_text,
        "match_type": match_type.upper(),
    }


@mcp.tool()
def update_campaign_budget(
    customer_id: str,
    budget_id: str,
    amount_micros: int,
) -> dict:
    """Update a campaign budget amount.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        budget_id: The campaign budget ID to update (query campaign.campaign_budget from campaign resource to find this)
        amount_micros: The new daily budget in micros (e.g., 10000000 = $10.00)
    """
    client = utils.get_googleads_client()
    budget_service = client.get_service("CampaignBudgetService")

    operation = client.get_type("CampaignBudgetOperation")
    budget = operation.update
    budget.resource_name = budget_service.campaign_budget_path(
        customer_id, budget_id
    )
    budget.amount_micros = amount_micros

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("amount_micros")
    operation.update_mask.CopyFrom(field_mask)

    response = budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_budget": response.results[0].resource_name,
        "new_amount": f"${amount_micros / 1_000_000:.2f}",
    }


@mcp.tool()
def update_ad_group_bid(
    customer_id: str,
    ad_group_id: str,
    cpc_bid_micros: int,
) -> dict:
    """Update the default CPC bid for an ad group.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to update
        cpc_bid_micros: The new CPC bid in micros (e.g., 1500000 = $1.50)
    """
    client = utils.get_googleads_client()
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group.cpc_bid_micros = cpc_bid_micros

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("cpc_bid_micros")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_ad_group": response.results[0].resource_name,
        "new_cpc_bid": f"${cpc_bid_micros / 1_000_000:.2f}",
    }


@mcp.tool()
def update_keyword_bid(
    customer_id: str,
    ad_group_id: str,
    criterion_id: str,
    cpc_bid_micros: int,
) -> dict:
    """Update the CPC bid for a specific keyword.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the keyword
        criterion_id: The keyword criterion ID to update
        cpc_bid_micros: The new CPC bid in micros (e.g., 1500000 = $1.50)
    """
    client = utils.get_googleads_client()
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.update
    criterion.resource_name = ad_group_criterion_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )
    criterion.cpc_bid_micros = cpc_bid_micros

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("cpc_bid_micros")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_keyword": response.results[0].resource_name,
        "new_cpc_bid": f"${cpc_bid_micros / 1_000_000:.2f}",
    }


@mcp.tool()
def remove_campaign(
    customer_id: str,
    campaign_id: str,
) -> dict:
    """Remove (delete) a campaign. This is permanent and cannot be undone.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        campaign_id: The campaign ID to remove
    """
    client = utils.get_googleads_client()
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    operation.remove = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "removed_campaign": response.results[0].resource_name,
    }


@mcp.tool()
def remove_ad_group(
    customer_id: str,
    ad_group_id: str,
) -> dict:
    """Remove (delete) an ad group. This is permanent and cannot be undone.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to remove
    """
    client = utils.get_googleads_client()
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    operation.remove = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "removed_ad_group": response.results[0].resource_name,
    }


@mcp.tool()
def remove_ad(
    customer_id: str,
    ad_group_id: str,
    ad_id: str,
) -> dict:
    """Remove (delete) an ad. This is permanent and cannot be undone.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID containing the ad
        ad_id: The ad ID to remove
    """
    client = utils.get_googleads_client()
    ad_group_ad_service = client.get_service("AdGroupAdService")

    operation = client.get_type("AdGroupAdOperation")
    operation.remove = ad_group_ad_service.ad_group_ad_path(
        customer_id, ad_group_id, ad_id
    )

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "removed_ad": response.results[0].resource_name,
    }


@mcp.tool()
def rename_campaign(
    customer_id: str,
    campaign_id: str,
    new_name: str,
) -> dict:
    """Rename a campaign.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        campaign_id: The campaign ID to rename
        new_name: The new campaign name
    """
    client = utils.get_googleads_client()
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign.name = new_name

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("name")
    operation.update_mask.CopyFrom(field_mask)

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_campaign": response.results[0].resource_name,
        "new_name": new_name,
    }


@mcp.tool()
def rename_ad_group(
    customer_id: str,
    ad_group_id: str,
    new_name: str,
) -> dict:
    """Rename an ad group.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to rename
        new_name: The new ad group name
    """
    client = utils.get_googleads_client()
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group.name = new_name

    field_mask = client.get_type("FieldMask")
    field_mask.paths.append("name")
    operation.update_mask.CopyFrom(field_mask)

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "updated_ad_group": response.results[0].resource_name,
        "new_name": new_name,
    }


@mcp.tool()
def create_ad_group(
    customer_id: str,
    campaign_id: str,
    name: str,
    cpc_bid_micros: Optional[int] = None,
    status: str = "ENABLED",
) -> dict:
    """Create a new ad group in a campaign.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        campaign_id: The campaign ID to create the ad group in
        name: The name for the new ad group
        cpc_bid_micros: Optional default CPC bid in micros (e.g., 1500000 = $1.50)
        status: The initial status: ENABLED or PAUSED (default ENABLED)
    """
    client = utils.get_googleads_client()
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = name
    ad_group.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    status_enum = client.enums.AdGroupStatusEnum
    ad_group.status = getattr(status_enum, status.upper())

    if cpc_bid_micros:
        ad_group.cpc_bid_micros = cpc_bid_micros

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "created_ad_group": response.results[0].resource_name,
        "name": name,
    }


@mcp.tool()
def create_responsive_search_ad(
    customer_id: str,
    ad_group_id: str,
    final_url: str,
    headlines: str,
    descriptions: str,
    path1: Optional[str] = None,
    path2: Optional[str] = None,
) -> dict:
    """Create a new Responsive Search Ad (RSA) in an ad group.

    Args:
        customer_id: The customer account ID (numbers only, no dashes)
        ad_group_id: The ad group ID to create the ad in
        final_url: The landing page URL for the ad
        headlines: JSON array of headline objects. Each object has "text" (required, max 30 chars) and optionally "pinned_field" (1=HEADLINE_1, 2=HEADLINE_2, 3=HEADLINE_3). Minimum 3, maximum 15 headlines.
        descriptions: JSON array of description objects. Each object has "text" (required, max 90 chars) and optionally "pinned_field" (1=DESCRIPTION_1, 2=DESCRIPTION_2). Minimum 2, maximum 4 descriptions.
        path1: Optional display URL path1 (max 15 chars, e.g., "caskets")
        path2: Optional display URL path2 (max 15 chars, e.g., "custom")
    """
    client = utils.get_googleads_client()
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_service = client.get_service("AdGroupService")

    headline_data = json.loads(headlines) if isinstance(headlines, str) else headlines
    description_data = json.loads(descriptions) if isinstance(descriptions, str) else descriptions

    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.create
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    ad.final_urls.append(final_url)

    pinned_field_map = {
        1: client.enums.ServedAssetFieldTypeEnum.HEADLINE_1,
        2: client.enums.ServedAssetFieldTypeEnum.HEADLINE_2,
        3: client.enums.ServedAssetFieldTypeEnum.HEADLINE_3,
    }
    pinned_desc_map = {
        1: client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1,
        2: client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_2,
    }

    for h in headline_data:
        ad_text_asset = client.get_type("AdTextAsset")
        ad_text_asset.text = h["text"]
        if h.get("pinned_field"):
            ad_text_asset.pinned_field = pinned_field_map.get(
                h["pinned_field"],
                client.enums.ServedAssetFieldTypeEnum.UNSPECIFIED,
            )
        ad.responsive_search_ad.headlines.append(ad_text_asset)

    for d in description_data:
        ad_text_asset = client.get_type("AdTextAsset")
        ad_text_asset.text = d["text"]
        if d.get("pinned_field"):
            ad_text_asset.pinned_field = pinned_desc_map.get(
                d["pinned_field"],
                client.enums.ServedAssetFieldTypeEnum.UNSPECIFIED,
            )
        ad.responsive_search_ad.descriptions.append(ad_text_asset)

    if path1:
        ad.responsive_search_ad.path1 = path1
    if path2:
        ad.responsive_search_ad.path2 = path2

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[operation],
    )

    return {
        "status": "success",
        "created_ad": response.results[0].resource_name,
        "final_url": final_url,
        "headline_count": len(headline_data),
        "description_count": len(description_data),
    }
