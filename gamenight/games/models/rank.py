from django.db import models


class Rank(models.Model):
    """The rank of a player in a game."""

    user = models.ForeignKey("games.User", on_delete=models.CASCADE)
    fixture = models.ForeignKey("games.Fixture", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(
        null=False,
        help_text="The rank of the individual player in a fixture.",
        default=0,
        blank=True,
    )
    team = models.CharField(
        max_length=100,
        null=False,
        help_text="The team the player is on. If empty, the player is not on a team.",
        blank=True,
        default="",
    )
    delta = models.IntegerField(
        default=0,
        editable=False,
        help_text="The change in score for the player, computed via the fixture graph.",
    )

    class Meta:
        constraints = (models.UniqueConstraint(fields=["user", "fixture"], name="unique_rank"),)
        ordering = ("rank",)

    def __str__(self) -> str:
        return f"{self.user.username[:5]} ({self.user.score}) {self.rank}"
