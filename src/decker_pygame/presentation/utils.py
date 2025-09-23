"""A collection of utility functions for the Pygame presentation layer.

This module provides helper functions for common tasks such as rendering wrapped
text, scaling surfaces, and ensuring sprites have valid `rect` attributes.
"""

import pygame


def get_and_ensure_rect(sprite: pygame.sprite.Sprite) -> pygame.Rect:
    """Gets a sprite's rect, creating it from the image if necessary.

    This is a defensive check to make composite sprites more robust. It ensures
    a sprite has a valid `rect` attribute and returns it.

    Args:
        sprite (pygame.sprite.Sprite): The sprite to validate.

    Returns:
        pygame.Rect: The sprite's valid pygame.Rect (or FRect).

    Raises:
        AttributeError: If the sprite is missing a `rect` and also lacks a
                        valid `image` from which a `rect` could be created.
    """
    if hasattr(sprite, "rect") and isinstance(sprite.rect, pygame.Rect):
        return sprite.rect
    if hasattr(sprite, "image") and isinstance(sprite.image, pygame.Surface):
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
    """Renders multi-line text onto a surface with word wrapping.

    This function modifies the provided surface in-place.

    Args:
        surface (pygame.Surface): The pygame.Surface to draw on.
        text (str): The string to render.
        font (pygame.font.Font): The pygame.font.Font to use.
        color (pygame.Color): The color of the text.
        rect (pygame.Rect): The pygame.Rect defining the bounds for wrapping.
        padding (int): The padding inside the rect.
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

            # If the new word itself is too long, we must break it.
            while font.size(current_line)[0] > max_width:
                # Find the character where the line breaks
                for i in range(1, len(current_line)):
                    if font.size(current_line[:i])[0] > max_width:
                        # If the break happens at i == 1, taking the
                        # previous slice yields an empty string and no
                        # progress is made. In that case, force a chunk
                        # of the first character so we make progress.
                        if i == 1:
                            lines.append(current_line[0])
                            current_line = current_line[1:]
                        else:
                            # The break happens at the previous character
                            lines.append(current_line[: i - 1])
                            current_line = current_line[i - 1 :]
                        break
                else:
                    # If we didn't break out of the loop, the first
                    # character is already wider than max_width. To avoid
                    # an infinite loop, force a break at the first
                    # character so progress is made.
                    lines.append(current_line[0])
                    current_line = current_line[1:]
    if current_line:
        lines.append(current_line)

    # Remove any empty lines introduced by splitting/chunking logic so we
    # don't call font.render with an empty string. Keep original order.
    filtered_lines = [ln for ln in lines if ln]
    for i, line in enumerate(filtered_lines):
        rendered_text = font.render(line, True, color)
        surface.blit(
            rendered_text, (rect.x + padding, rect.y + padding + i * line_height)
        )


def scale_icons(
    icons: list[pygame.Surface], target_size: tuple[int, int]
) -> list[pygame.Surface]:
    """Scales a list of pygame.Surface objects to a target size.

    Args:
        icons (list[pygame.Surface]): A list of surfaces to scale.
        target_size (tuple[int, int]): The (width, height) to scale to.

    Returns:
        list[pygame.Surface]: A new list of scaled surfaces.
    """
    return [pygame.transform.scale(icon, target_size) for icon in icons]
