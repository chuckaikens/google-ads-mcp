"""Tools for mutating Google Ads resources (ads, campaigns, ad groups, keywords)."""

from typing import Optional
from ads_mcp.coordinator import mcp
import ads_mcp.utils as utils


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

    status_enum = client.enums.AdGroupAdStatusEnum.AdGroupAdStatus
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

    status_enum = client.enums.CampaignStatusEnum.CampaignStatus
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

    status_enum = client.enums.AdGroupStatusEnum.AdGroupStatus
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

    status_enum = client.enums.AdGroupCriterionStatusEnum.AdGroupCriterionStatus
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
    criterion.status = client.enums.AdGroupCriterionStatusEnum.AdGroupCriterionStatus.ENABLED
    criterion.keyword.text = keyword_text
    criterion.keyword.match_type = getattr(
        client.enums.KeywordMatchTypeEnum.KeywordMatchType, match_type.upper()
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
        client.enums.KeywordMatchTypeEnum.KeywordMatchType, match_type.upper()
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
        client.enums.KeywordMatchTypeEnum.KeywordMatchType, match_type.upper()
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
