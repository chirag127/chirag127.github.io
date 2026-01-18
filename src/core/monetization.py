"""
Monetization Configuration - Centralized monetization settings.

All monetization integrations for PRFusion-generated repositories.
Includes ads, donations, affiliate links, and crypto wallets.
"""

from dataclasses import dataclass, field
from typing import Dict, Any

from src.core.config import Settings


@dataclass
class UserProfile:
    """User profile for attribution and branding."""
    name: str = "Chirag Singhal"
    email: str = "whyiswhen@gmail.com"
    github_username: str = "chirag127"
    website_url: str = Settings.SITE_BASE_URL
    role: str = "Software Engineer · Backend & GenAI Specialist"
    location: str = "Bhubaneswar, Odisha, India"
    education: str = "B.Tech in CSE (8.81 CGPA) from Dr. A.P.J. Abdul Kalam Technical University (2020-2024)"


@dataclass
class AAdsConfig:
    """A-Ads crypto advertising configuration."""
    enabled: bool = True
    unit_id: str = "2424216"

    @property
    def iframe_code(self) -> str:
        return f'''<div id="a-ads-frame" style="width: 100%; margin: auto; position: relative; z-index: 99998;">
    <iframe data-aa="{self.unit_id}"
            src="//acceptable.a-ads.com/{self.unit_id}/?size=Adaptive"
            style="border:0; padding:0; width:70%; height:auto; overflow:hidden; display: block; margin: auto">
    </iframe>
</div>'''


@dataclass
class BuyMeACoffeeConfig:
    """Buy Me a Coffee donation configuration."""
    enabled: bool = True
    username: str = "chirag127"

    @property
    def url(self) -> str:
        return f"https://buymeacoffee.com/{self.username}"

    @property
    def widget_code(self) -> str:
        return f'''<script data-name="BMC-Widget" data-cfasync="false"
    src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js"
    data-id="{self.username}"
    data-description="Support me on Buy me a coffee!"
    data-message="Thank you for visiting! Consider supporting my work."
    data-color="#5F7FFF"
    data-position="Right"
    data-x_margin="18"
    data-y_margin="18">
</script>'''

    @property
    def badge_markdown(self) -> str:
        return f"[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)]({self.url})"


@dataclass
class GitHubSponsorsConfig:
    """GitHub Sponsors configuration."""
    enabled: bool = True
    username: str = "chirag127"

    @property
    def url(self) -> str:
        return f"https://github.com/sponsors/{self.username}"

    @property
    def badge_markdown(self) -> str:
        return f"[![Sponsor](https://img.shields.io/badge/Sponsor-EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white)]({self.url})"


@dataclass
class AmazonAssociatesConfig:
    """Amazon Associates affiliate configuration."""
    enabled: bool = True
    store_id: str = "chirag127-21"
    marketplace: str = "amazon.in"

    def product_link(self, asin: str) -> str:
        """Generate affiliate link for a product."""
        return f"https://www.{self.marketplace}/dp/{asin}?tag={self.store_id}"


@dataclass
class CryptoWallets:
    """Cryptocurrency wallet addresses for donations."""
    btc: str = "bc1qextzy9thrsta6l355kuwdvggehkkmky0zzjnfl"
    eth: str = "0xee4e65aa41bfb2d6649c9d3787ff4747704198de"
    sol: str = "C4nXxdbUrpTHsEHm5kPfqCVgVbx5cbD5yZNeBbyzyQSi"

    def html_section(self) -> str:
        """Generate HTML section for crypto donations."""
        return f'''<div class="crypto-donations">
    <h4>🪙 Crypto Donations</h4>
    <div class="crypto-address">
        <strong>Bitcoin (BTC):</strong>
        <code>{self.btc}</code>
    </div>
    <div class="crypto-address">
        <strong>Ethereum (ETH):</strong>
        <code>{self.eth}</code>
    </div>
    <div class="crypto-address">
        <strong>Solana (SOL):</strong>
        <code>{self.sol}</code>
    </div>
</div>'''


@dataclass
class UPIConfig:
    """UPI payment configuration (India)."""
    enabled: bool = True
    upi_id: str = "jiochirag127@ybl"

    @property
    def payment_link(self) -> str:
        return f"upi://pay?pa={self.upi_id}"

    def html_section(self) -> str:
        return f'''<div class="upi-donation">
    <h4>💳 UPI Payment (India)</h4>
    <p>UPI ID: <code>{self.upi_id}</code></p>
</div>'''


@dataclass
class BankTransferConfig:
    """Bank transfer information for business inquiries."""
    enabled: bool = True
    bank_name: str = "Kotak Mahindra Bank"
    ifsc: str = "KKBK0000677"
    swift_code: str = "KKBKINBB"
    note: str = "For business inquiries or direct wire transfers."


@dataclass
class MonetizationConfig:
    """Complete monetization configuration."""
    user_profile: UserProfile = field(default_factory=UserProfile)
    a_ads: AAdsConfig = field(default_factory=AAdsConfig)
    buy_me_a_coffee: BuyMeACoffeeConfig = field(default_factory=BuyMeACoffeeConfig)
    github_sponsors: GitHubSponsorsConfig = field(default_factory=GitHubSponsorsConfig)
    amazon_associates: AmazonAssociatesConfig = field(default_factory=AmazonAssociatesConfig)
    crypto_wallets: CryptoWallets = field(default_factory=CryptoWallets)
    upi: UPIConfig = field(default_factory=UPIConfig)
    bank_transfer: BankTransferConfig = field(default_factory=BankTransferConfig)

    def get_readme_support_section(self) -> str:
        """Generate markdown section for README files."""
        return f"""## ❤️ Support

If you find this project helpful, please consider supporting:

{self.buy_me_a_coffee.badge_markdown}
{self.github_sponsors.badge_markdown}

### 🪙 Crypto Donations

| Currency | Address |
|----------|---------|
| **BTC** | `{self.crypto_wallets.btc}` |
| **ETH** | `{self.crypto_wallets.eth}` |
| **SOL** | `{self.crypto_wallets.sol}` |

### 💳 UPI (India)

UPI ID: `{self.upi.upi_id}`

---

**Made with ❤️ by [{self.user_profile.name}]({self.user_profile.website_url})**
"""

    def get_footer_html(self) -> str:
        """Generate HTML footer with all attribution and monetization."""
        import datetime
        year = datetime.datetime.now().year

        return f'''<footer class="site-footer">
    <div class="footer-content">
        <div class="footer-brand">
            <p>&copy; {year} {self.user_profile.name}. All rights reserved.</p>
            <p>{self.user_profile.role}</p>
        </div>

        <div class="footer-links">
            <a href="https://github.com/{self.user_profile.github_username}" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white" alt="GitHub">
            </a>
            <a href="{self.buy_me_a_coffee.url}" target="_blank">
                <img src="https://img.shields.io/badge/Buy%20Me%20Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee">
            </a>
            <a href="{self.github_sponsors.url}" target="_blank">
                <img src="https://img.shields.io/badge/Sponsor-EA4AAA?style=flat&logo=github-sponsors&logoColor=white" alt="Sponsor">
            </a>
        </div>

        <div class="footer-nav">
            <a href="privacy.html">Privacy Policy</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        </div>
    </div>

    {self.a_ads.iframe_code}
    {self.buy_me_a_coffee.widget_code}
</footer>'''

    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary (for JSON templates)."""
        return {
            "user_profile": {
                "name": self.user_profile.name,
                "email": self.user_profile.email,
                "github_username": self.user_profile.github_username,
                "website_url": self.user_profile.website_url,
                "role": self.user_profile.role
            },
            "monetization": {
                "a_ads": {
                    "enabled": self.a_ads.enabled,
                    "unit_id": self.a_ads.unit_id
                },
                "buy_me_a_coffee": {
                    "enabled": self.buy_me_a_coffee.enabled,
                    "username": self.buy_me_a_coffee.username,
                    "url": self.buy_me_a_coffee.url
                },
                "github_sponsors": {
                    "enabled": self.github_sponsors.enabled,
                    "url": self.github_sponsors.url
                },
                "amazon_associates": {
                    "enabled": self.amazon_associates.enabled,
                    "store_id": self.amazon_associates.store_id
                },
                "crypto_wallets": {
                    "btc": self.crypto_wallets.btc,
                    "eth": self.crypto_wallets.eth,
                    "sol": self.crypto_wallets.sol
                },
                "upi": {
                    "id": self.upi.upi_id
                },
                "bank_transfer": {
                    "bank_name": self.bank_transfer.bank_name,
                    "ifsc": self.bank_transfer.ifsc,
                    "swift_code": self.bank_transfer.swift_code
                }
            }
        }


# Singleton instance for easy import
MONETIZATION = MonetizationConfig()
