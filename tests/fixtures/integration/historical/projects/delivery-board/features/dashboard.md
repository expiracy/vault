# Delivery dashboard

Feature identifier: `delivery-dashboard`. Synthetic test fixture.

## Current design

Fixture baseline: the dashboard displays delivery IDs and their status in input order. There are no filters. These are supplied fixture assumptions; no deployed application or code implementation is present in this repository. Runtime verification is not established.

## Identified changes

### Change dashboard-filters

Origin: [dashboard filter design task](../tasks/dashboard-filters/context.md). Proposed on 11 October 2026; documentation-only scope.

| Decision | Implementation | Verification |
| --- | --- | --- |
| `proposed` | `not-started` | `not-checked` |

These states concern the filter change. Documentation review does not establish runtime behaviour.

#### Controls and defaults

Add a single-select **Status** control, **Delivery date from** and **Delivery date to** inputs, **Apply** and **Clear filters** above the existing list. Status defaults to **All statuses**; both dates start blank. Status options use the distinct canonical values supplied by the existing delivery input; labels map to those values without inventing a status vocabulary.

Apply replaces the active filters only when all supplied values are valid. Reject an unknown status, an invalid calendar date, or a from date later than the to date; show an inline error beside the affected control. Invalid drafts leave the previous active filters and results intact. Clear filters immediately resets the controls and active filters to their defaults. This explicit apply step lets users finish a date range before changing results.

With no active filters, retain the original IDs and statuses in input order. Filtering removes rows without changing their order or displayed fields. When active filters match no deliveries, show **No deliveries match these filters** and retain the controls so users can adjust or clear them. An empty unfiltered list keeps its existing empty behaviour.

#### Matching and date contract

Each supplied condition must match: status equality **AND** date on or after from **AND** date on or before to. An unset condition evaluates to true. Either date bound can be supplied alone; bounds are inclusive.

Propose a per-delivery `deliveryDate` calendar date in `YYYY-MM-DD` form, used only for filtering. Missing or malformed record dates cannot match an active date bound; they remain eligible when neither bound is active. Dates compare as calendar dates without implicit timezone conversion.

The fixture defines no date field. **Review dependency:** confirm the delivery-date source and its calendar meaning before accepting or implementing this contract. If the source is a timestamp, agree its timezone-to-date conversion first. This is a proposed data requirement, not an observed field.

```text
Deliveries in input order
          |
          v
Status matches AND date >= from AND date <= to
          (unset conditions are true)
          |
          v
Matching IDs and statuses, preserving input order
```

#### Review cases

| Case | Required result |
| --- | --- |
| No filters, including after Clear filters | Original list, fields and order. |
| Status only | Exact status matches; missing dates do not exclude rows. |
| From only / to only | Apply only that inclusive bound. |
| Same from and to date | Include that calendar date only. |
| Status and date bounds | Exclude a row if either status or any supplied bound fails. |
| Missing or malformed record date | Exclude only when a date bound is active. |
| Invalid draft / no matches | Keep active filters and results on error; otherwise show the filtered empty state. |

These cases specify future behaviour. No application checks have been run.

## History

The original list-delivery scope is preserved in [its checkpoint](../tasks/delivery-list/context.md#completion-checkpoint-delivery-list).

The later filter proposal is recorded separately in [its task context](../tasks/dashboard-filters/context.md).
