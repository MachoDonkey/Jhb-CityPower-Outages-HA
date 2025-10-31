FROM python:3.11-slim

# Basic deps for Home Assistant
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libffi-dev \
     libssl-dev \
     libjpeg-dev \
     zlib1g-dev \
     git \
     ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME || true \
 && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME || true

WORKDIR /workspace

# Install Home Assistant (core). This is a simple dev install and may be
# adjusted to match your preferred HA development flow.
RUN python -m pip install --upgrade pip
RUN pip install homeassistant

# Create a config directory mount point
RUN mkdir -p /config
RUN chown -R $USERNAME:$USERNAME /config /workspace

USER $USERNAME

ENV PATH="/home/$USERNAME/.local/bin:$PATH"

CMD ["/bin/bash"]
