from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network,accounts, exceptions
import pytest


def test_can_fund_and_widthdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# brownie test -k test_only_owner_can_withdraw() --network rinkeby
# @pytest.mark.require_network("rinkeby")
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    
    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})



# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/necI_Y2qp6jZS_HNwIsdS9t7A2rdomyS accounts=10 mnemonic=brownie port=8545
# brownie run scripts/deploy.py --network mainnet-fork-dev
# brownie test --network mainnet-fork-dev
# git init -b main