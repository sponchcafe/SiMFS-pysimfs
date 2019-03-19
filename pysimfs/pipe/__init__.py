from platform import platform

platform_name = platform()

if platform_name.startswith('Darwin') or platform_name.startswith('Linux'):
    from . unix_pipe import UnixPipe as Pipe
elif platform().startswith('Windows'):
    from . win_pipe import WinPipe as Pipe
else:
    from . pipe import BasePipe as Pipe
    raise ImportError(f'Platform {platform()} not recognized')
