import pygame


def get_and_ensure_rect(sprite: pygame.sprite.Sprite) -> pygame.Rect:
    """
    Gets a sprite's rect, creating it from the image if necessary.

    This is a defensive check to make composite sprites more robust. It ensures
    a sprite has a valid `rect` attribute and returns it.

    Args:
        sprite: The sprite to validate.

    Returns:
        The sprite's valid pygame.Rect (or FRect).

    Raises:
        AttributeError: If the sprite is missing a `rect` and also lacks a
                        valid `image` from which a `rect` could be created.
    """
    if (
        hasattr(sprite, "rect")
        and sprite.rect is not None
        and isinstance(sprite.rect, pygame.Rect)
    ):
        return sprite.rect
    if hasattr(sprite, "image") and sprite.image is not None:
        sprite.rect = sprite.image.get_rect()
        return sprite.rect

    raise AttributeError(
        f"Cannot get rect for sprite {sprite}:\n"
        "  it has no 'rect' or a valid 'image' attribute."
    )


def render_text_wrapped(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    rect: pygame.Rect,
    padding: int = 0,
) -> None:
    """
    Renders multi-line text onto a surface with word wrapping.

    This function modifies the provided surface in-place.

    Args:
        surface: The pygame.Surface to draw on.
        text: The string to render.
        font: The pygame.font.Font to use.
        color: The color of the text.
        rect: The pygame.Rect defining the bounds for wrapping.
        padding: The padding inside the rect.
    """
    words = text.split()
    lines = []
    current_line = ""
    max_width = rect.width - (padding * 2)
    line_height = font.get_linesize()

    for word in words:
        test_line = f"{current_line} {word}" if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        surface.blit(
            rendered_text, (rect.x + padding, rect.y + padding + i * line_height)
        )


def scale_icons(
    icons: list[pygame.Surface], target_size: tuple[int, int]
) -> list[pygame.Surface]:
    """
    Scales a list of pygame.Surface objects to a target size.

    Args:
        icons: A list of surfaces to scale.
        target_size: The (width, height) to scale to.

    Returns:
        A new list of scaled surfaces.
    """
    return [pygame.transform.scale(icon, target_size) for icon in icons]
