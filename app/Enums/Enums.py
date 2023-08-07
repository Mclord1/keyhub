import enum


class GenderEnums(enum.Enum):
    male = "Male"
    female = "Female"
    not_selected = "Prefer not to say"


class AccountTierEnum(enum.Enum):
    TIER_1 = "TIER 1"
    TIER_2 = "TIER 2"


class VerificationEnum(enum.Enum):
    PENDING = "pending"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class VerificationTypeEnum(enum.Enum):
    BVN = 'BVN'
    CAC = 'CAC'
    NIN = 'NIN'
    ID_CARD = 'ID_CARD'
    PASSPORT = 'PASSPORT'
    DRIVING_LICENSE = 'DRIVING_LICENSE'


class ReferralStatusEnum(enum.Enum):
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"
    COMPLETED = "COMPLETED"


class AccountTypeEnum(enum.Enum):
    BUSINESS = "BUSINESS"
    PERSONAL = 'PERSONAL'


class LoanTypeEnum(enum.Enum):
    QUICKLOAN = 'QUICKLOAN'
    OVERDRAFT = 'OVERDRAFT'
    P2P = 'P2P'


class NotificationClassesEnum(enum.Enum):
    TRANSACTION = 'Transaction'
    NEW_CARD = 'New_Card_Issue'
    AMEND_REGULAR_PAYMENT = 'Amend_Regular_Payment'
    UPDATE_CONTACT = 'Update_Contact_Details'
    UNRECOGNIZED_LOCATION = 'Unrecognized_Location'


class NotificationStatusEnum(enum.Enum):
    READ = 'READ'
    UNREAD = 'UNREAD'
