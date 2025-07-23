### AgentDrop

This agent facilitates the distribution of 2 NEAR tokens to eligible participants of the "One Trillion Agents Hackathon." It guides users through the process of verifying their DevPost profile to claim the tokens.

**Main Functions:**

*   **DevPost Profile Verification:** Analyzes user-provided DevPost profile links to ensure they meet specific criteria, including:
    *   Being a registered participant of the hackathon.
    *   Having the "near.ai" skill tag.
    *   Including a specific message in their bio with their NEAR account ID.
    *   Not having been previously funded.
*   **NEAR Token Distribution:** Upon successful verification, the agent initiates a transaction to transfer 2 NEAR tokens to the user's specified NEAR account via a smart contract.
*   **User Guidance:** Provides clear instructions and feedback to users throughout the claiming process.

**Inputs:**

*   **Chat Message (text):** User provides a DevPost profile link.

**Outputs:**

*   **Chat Message (text):**
    *   Instructions on how to qualify for and claim the tokens.
    *   Validation results (e.g., "link is not DevPost," "profile already funded," "missing skill tag," "missing bio message").
    *   Confirmation of successful funding with a link to the NEAR transaction on NearBlocks.
    *   Error messages if an issue occurs during the process.

**Environment Variables:**

*   **`FAUCET_ACCOUNT_ID`**: The NEAR account ID of the smart contract responsible for distributing the funds. Defaults to "1t-agents-fund.frol.near".
*   **`FAUCET_PRIVATE_ACCESS_KEY_2`**: The private access key required for the agent to authorize transactions (e.g., calling the `fund` method) on behalf of the `FAUCET_ACCOUNT_ID`. This is a mandatory configuration.