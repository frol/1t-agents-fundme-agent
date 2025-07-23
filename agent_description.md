### AgentDrop

AgentDrop is an agent designed to distribute 2 NEAR tokens to eligible participants of the "One Trillion Agents Hackathon." It automates the process of verifying participant eligibility and funding their NEAR accounts via a smart contract.

**Main Functions:**

*   **DevPost Profile Validation:** Analyzes user-provided DevPost profile links to ensure they are valid, belong to a registered hackathon participant, and meet specific criteria (e.g., presence of "near.ai" skill tag and a bio message containing a NEAR account ID).
*   **NEAR Token Distribution:** Interacts with a NEAR smart contract to check if a profile has already been funded and, if not, initiates a transfer of 2 NEAR tokens to the specified NEAR account.
*   **User Communication:** Guides users through the funding process, provides feedback on validation steps, and confirms successful funding or explains reasons for failure.

**Inputs:**

*   **Chat Message (text):** User provides their DevPost profile link as a chat message.

**Outputs:**

*   **Chat Reply (text):** The agent responds with instructions, validation results, funding status, or error messages.

**Environment Variables:**

*   **`FAUCET_ACCOUNT_ID`**: The NEAR account ID of the faucet smart contract used for token distribution. Defaults to `1t-agents-fund.frol.near`.
*   **`FAUCET_PRIVATE_ACCESS_KEY_2`**: The private access key for the faucet account, required to sign transactions for token transfers. This variable is mandatory.