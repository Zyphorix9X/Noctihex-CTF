# NHX-05 outbound isolation — fixed and retested

The earlier ordinary challenge access bridge failed isolation. The approved SSH gateway is deployed, and both challenges attach only to internal networks. The user-run completion script produced seven passing integration checks, eleven passing controlled isolation checks after reset, two passing reset checks and 59 passing player checks. Persistent SSH host identity is checked by reset-test.py. Evidence is under testing/test-results/ and testing/reset-tests/.
