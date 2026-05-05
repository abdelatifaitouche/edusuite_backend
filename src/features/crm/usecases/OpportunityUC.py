from src.db.usecases.base_usecase import BaseUC
from src.features.crm.schemas.opportunity import (
    ReadOpporunity,
    CreateOpportunity,
    UpdateOpportunity,
)
from uuid import UUID
from typing import override
from src.features.crm.domaine.opportunity import Opportunity as OpportunityEntity
from src.features.crm.enums.opportunity_states import OpportunityStates
from src.core.pagination import Pagination
from src.features.crm.repository.opportunity_repo import OpportunityRepo
from src.core.exception import NotFoundError


class OpportunityUC(BaseUC[OpportunityEntity, CreateOpportunity, UpdateOpportunity]):
    ALLOWED_TRANSITIONS = {
        OpportunityStates.NEW: [
            OpportunityStates.NEED_ANALYSIS,
            OpportunityStates.LOST,
        ],
        OpportunityStates.NEED_ANALYSIS: [
            OpportunityStates.PROPOSAL,
            OpportunityStates.LOST,
        ],
        OpportunityStates.PROPOSAL: [
            OpportunityStates.NEGOTIATION,
            OpportunityStates.LOST,
        ],
        OpportunityStates.NEGOTIATION: [OpportunityStates.WON, OpportunityStates.LOST],
        OpportunityStates.WON: [],
        OpportunityStates.LOST: [],
    }
    PIPELINE: list[OpportunityStates] = [
        OpportunityStates.NEW,
        OpportunityStates.NEED_ANALYSIS,
        OpportunityStates.PROPOSAL,
        OpportunityStates.NEGOTIATION,
        OpportunityStates.WON,
        OpportunityStates.LOST,
    ]

    def __init__(self, repo: OpportunityRepo):
        super().__init__(repo=repo)
        self.repo: OpportunityRepo = repo

    def _to_entity(self, data: CreateOpportunity) -> OpportunityEntity:
        return OpportunityEntity(
            title=data.title,
            probability=data.probability,
            expected_close_date=data.expected_close_date,
            estimated_value=data.estimated_value,
            status=data.status,
        )

    async def get_by_id(self, entity_id: UUID) -> OpportunityEntity:

        result = await self.repo.get_by_id(entity_id)

        if not result:
            raise NotFoundError(message=f"With ID {entity_id} was not Found")

        return result

    async def list(
        self, pagination: Pagination, filters=None
    ) -> list[OpportunityEntity]:
        return await self.repo.list_opportunities(pagination, filters)

    async def create(self, data: CreateOpportunity) -> OpportunityEntity:
        if data.probability <= 0 or data.probability > 1:
            raise Exception("Error in Probability")
        from datetime import date

        if data.expected_close_date <= date.today():
            raise Exception("Datetime error")

        return await super().create(data)

    async def mark_as_win(self, entity_id: UUID) -> OpportunityEntity:
        entity: OpportunityEntity = await self.get_by_id(entity_id)

        if not self._can_transition(entity.status, OpportunityStates.WON):
            raise Exception("Invalid State transition")

        entity.status = OpportunityStates.WON

        return await self.repo.save(entity)

    async def mark_as_lost(self, entity_id: UUID):
        """
        DUPLICATED CODE NEEDS TO REFACTOR LATEER
        """

        entity: OpportunityEntity = await self.get_by_id(entity_id)

        if not self._can_transition(entity.status, OpportunityStates.LOST):
            raise Exception("Invalid State transition")

        entity.status = OpportunityStates.LOST

        return await self.repo.save(entity)

    async def transition(self, entity_id: UUID):

        entity = await self.get_by_id(entity_id)

        if not entity.status:
            raise Exception("No status")

        next_stage: OpportunityStates | None = self.get_next_stage(entity.status)

        if next_stage == OpportunityStates.PROPOSAL:
            if entity.session_plan_id is None:
                raise Exception("A session Plan needs to be created first")

        if not next_stage:
            raise Exception(
                f"No next stage, current stage{entity.status}, next {next_stage}"
            )

        entity.status = next_stage

        return await self.repo.save(entity)

    def get_next_stage(self, current_stage: OpportunityStates):

        if (
            current_stage == OpportunityStates.LOST
            or current_stage == OpportunityStates.WON
        ):
            return

        current_stage_idx: int = self.PIPELINE.index(current_stage)
        next_stage = self.PIPELINE[current_stage_idx + 1]
        if not self._can_transition(current_stage, next_stage):
            raise Exception("cannot transition")
        return next_stage

    def _can_transition(
        self, current_state: OpportunityStates, next_state: OpportunityStates
    ) -> bool:
        print(self.ALLOWED_TRANSITIONS[current_state])
        if next_state in self.ALLOWED_TRANSITIONS[current_state]:
            return True

        return False

    async def delete(self, entity_id: UUID):
        entity: OpportunityEntity = await self.get_by_id(entity_id)

        if entity.status != OpportunityStates.NEW:
            raise Exception("Invalid state to delete")

        return await super().delete(entity_id)
