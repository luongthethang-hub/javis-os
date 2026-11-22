"""Deterministic, single-position research model for OTC Bid/Ask ticks."""

from collections import deque
from dataclasses import dataclass
from types import SimpleNamespace

from .data import RECORD

TRADE_FIELDS = (
    "side", "entry_time_msc", "exit_time_msc", "entry_seq", "exit_seq",
    "entry_price_points", "exit_price_points", "reason", "pnl_points",
)
PARITY_FIELDS = (
    "side", "entry_time_msc", "exit_time_msc", "entry_price_points",
    "exit_price_points", "reason",
)


@dataclass(frozen=True)
class Settings:
    bar_minutes: int
    fast: int
    slow: int
    stop_points: int
    target_points: int
    slippage_points: int = 0
    fee_points: int = 0
    direction: str = "both"

    def __post_init__(self):
        if not 1 <= self.bar_minutes <= 1440 or not 1 <= self.fast < self.slow <= 10000:
            raise ValueError("Cần timeframe 1-1440 phút và 1 <= fast < slow <= 10000.")
        if not 1 <= min(self.stop_points, self.target_points) <= max(self.stop_points, self.target_points) <= 10**12:
            raise ValueError("SL và TP phải nằm trong [1, 10^12] points.")
        if not 0 <= min(self.slippage_points, self.fee_points) <= max(self.slippage_points, self.fee_points) <= 10**12:
            raise ValueError("Slippage và phí phải nằm trong [0, 10^12] points.")
        if self.direction not in ("both", "long", "short"):
            raise ValueError("direction không hợp lệ.")


def lower_bound(mapped, stamp):
    low, high = 0, len(mapped) // RECORD.size
    while low < high:
        mid = (low + high) // 2
        if int.from_bytes(mapped[mid * RECORD.size:mid * RECORD.size + 8], "little", signed=True) < stamp:
            low = mid + 1
        else:
            high = mid
    return low


def replay(mapped, settings, write_trade=None, chart_limit=600, start_ms=None, end_ms=None):
    if start_ms is not None and end_ms is not None and start_ms >= end_ms:
        raise ValueError("Khoảng replay phải thỏa start < end.")
    begin = lower_bound(mapped, start_ms) if start_ms is not None else 0
    stop_at = lower_bound(mapped, end_ms) if end_ms is not None else len(mapped) // RECORD.size
    if begin == stop_at:
        raise ValueError("Khoảng replay không chứa tick.")
    period = settings.bar_minutes * 60_000
    fast_window, slow_window = deque(), deque()
    fast_sum = slow_sum = relation = 0
    ready = False
    candles = deque(maxlen=chart_limit)
    markers = deque(maxlen=chart_limit * 4)
    candle_start = None
    open_price = high = low = close = candle_ticks = bars = 0
    usable = invalid = blocked = signals = 0
    position = None
    settled = gross_gain = gross_loss = drawdown = peak = wins = losses = flat = 0
    last_quote = None
    direction = {"both": 0, "long": 1, "short": -1}[settings.direction]
    slip, fee = settings.slippage_points, settings.fee_points

    def settle(seq, stamp, price, reason):
        nonlocal settled, gross_gain, gross_loss, wins, losses, flat, position
        side = "long" if position.side == 1 else "short"
        pnl = position.side * (price - position.price) - fee
        settled += pnl
        gross_gain += max(pnl, 0)
        gross_loss += max(-pnl, 0)
        wins += pnl > 0
        losses += pnl < 0
        flat += pnl == 0
        if write_trade is not None:
            write_trade((side, position.stamp, stamp, position.seq, seq, position.price, price, reason, pnl))
        if chart_limit:
            markers.append((stamp, price, "exit", side, reason))
        position = None

    def update_equity(equity):
        nonlocal peak, drawdown
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)

    with memoryview(mapped) as view, view[begin * RECORD.size:stop_at * RECORD.size] as region:
        unpacked = RECORD.iter_unpack(region)
        try:
            for seq, (stamp, bid, ask, _, _, _, _) in enumerate(unpacked, begin + 1):
                if not bid or not ask:
                    invalid += 1
                    continue
                usable += 1
                last_quote = seq, stamp, bid, ask
                closed_this_tick = False
                if position is not None:
                    quote = bid if position.side == 1 else ask
                    if position.side * (quote - position.stop) <= 0:
                        settle(seq, stamp, max(1, quote - position.side * slip), "SL")
                        closed_this_tick = True
                    elif position.side * (quote - position.target) >= 0:
                        settle(seq, stamp, max(1, quote - position.side * slip), "TP")
                        closed_this_tick = True

                bucket = stamp // period * period
                if bucket != candle_start:
                    enter = 0
                    if candle_start is not None:
                        if chart_limit:
                            candles.append((candle_start, open_price, high, low, close, candle_ticks))
                        bars += 1
                        # Drop the first sampled candle from warm-up. It may start mid-bar.
                        if bars > 1:
                            fast_window.append(close)
                            slow_window.append(close)
                            fast_sum += close
                            slow_sum += close
                            if len(fast_window) > settings.fast:
                                fast_sum -= fast_window.popleft()
                            if len(slow_window) > settings.slow:
                                slow_sum -= slow_window.popleft()
                            if len(slow_window) == settings.slow:
                                difference = fast_sum * settings.slow - slow_sum * settings.fast
                                next_relation = (difference > 0) - (difference < 0)
                                if ready and next_relation and next_relation != relation:
                                    enter = next_relation
                                relation = next_relation
                                ready = True

                    candle_start = bucket
                    open_price = high = low = close = bid
                    candle_ticks = 1
                    if enter and (not direction or direction == enter):
                        signals += 1
                        if position is None and not closed_this_tick:
                            entry = (ask + slip) if enter == 1 else (bid - slip)
                            sl = entry - enter * settings.stop_points
                            tp = entry + enter * settings.target_points
                            exit_quote = bid if enter == 1 else ask
                            if min(entry, sl, tp) > 0 and enter * (exit_quote - sl) > 0:
                                position = SimpleNamespace(
                                    side=enter, price=entry, stop=sl, target=tp, seq=seq, stamp=stamp,
                                )
                                if chart_limit:
                                    markers.append((stamp, entry, "entry", "long" if enter == 1 else "short", "SMA"))
                            else:
                                blocked += 1
                else:
                    close = bid
                    high = max(high, bid)
                    low = min(low, bid)
                    candle_ticks += 1

                if position is None:
                    update_equity(settled)
                else:
                    mark = bid if position.side == 1 else ask
                    update_equity(settled + position.side * (mark - position.price) - fee)
        finally:
            del unpacked

    if last_quote is None:
        raise ValueError("Khoảng replay không có quote Bid/Ask khả dụng.")
    if chart_limit:
        candles.append((candle_start, open_price, high, low, close, candle_ticks))
    if position is not None:
        seq, stamp, bid, ask = last_quote
        quote = bid if position.side == 1 else ask
        settle(seq, stamp, max(1, quote - position.side * slip), "END")
        update_equity(settled)

    return {
        "ticks": usable + invalid, "valid_quotes": usable, "skipped_quotes": invalid,
        "signals": signals, "invalid_stop_entries": blocked, "bars": bars + 1,
        "trades": wins + losses + flat, "wins": wins, "losses": losses, "flat": flat,
        "net_points": settled, "gross_gain_points": gross_gain, "gross_loss_points": gross_loss,
        "profit_factor": gross_gain / gross_loss if gross_loss else None,
        "profit_factor_unbounded": bool(gross_gain and not gross_loss),
        "max_mark_to_market_drawdown_points": drawdown,
        "bars_tail": list(candles), "markers_tail": list(markers),
    }

