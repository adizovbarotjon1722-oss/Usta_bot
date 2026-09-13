from aiogram.fsm.state import State, StatesGroup


class CustomerOrder(StatesGroup):
    choosing_service = State()
    entering_description = State()
    sending_location = State()
    entering_address_text = State()
    sending_phone = State()
    choosing_master = State()


class MasterRegister(StatesGroup):
    entering_name = State()
    entering_age = State()
    entering_experience = State()
    entering_passport = State()
    sending_criminal_record = State()
    sending_qualification = State()
    entering_phone = State()
    entering_extra_phone = State()
    choosing_service = State()
    sending_location = State()
    sending_photo = State()


class Onboarding(StatesGroup):
    choosing_language = State()


class ReviewComment(StatesGroup):
    entering_comment = State()


class WarrantyClaim(StatesGroup):
    entering_issue = State()


class MasterPricing(StatesGroup):
    entering_price = State()
    confirming_low_price = State()


class TopUp(StatesGroup):
    entering_amount = State()


class SupportMessage(StatesGroup):
    entering_message = State()


class AdminActions(StatesGroup):
    entering_reply_target = State()
    entering_reply_text = State()
    entering_balance_master_id = State()
    entering_balance_amount = State()
    entering_block_master_id = State()
    entering_unblock_master_id = State()
    entering_fund_payout_amount = State()
    entering_fund_payout_reason = State()
    entering_block_customer_id = State()
    entering_unblock_customer_id = State()
    choosing_broadcast_target = State()
    entering_broadcast_text = State()
