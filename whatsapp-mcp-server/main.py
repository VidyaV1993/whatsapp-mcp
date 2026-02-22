from typing import List, Dict, Any, Optional
import json
import os
from mcp.server.fastmcp import FastMCP
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

@mcp.tool()
def search_contacts(query: str) -> List[Dict[str, Any]]:
    """Search WhatsApp contacts by name or phone number.
    
    Args:
        query: Search term to match against contact names or phone numbers
    """
    contacts = whatsapp_search_contacts(query)
    return contacts

@mcp.tool()
def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Dict[str, Any]]:
    """Get WhatsApp messages matching specified criteria with optional context.
    
    Args:
        after: Optional ISO-8601 formatted string to only return messages after this date
        before: Optional ISO-8601 formatted string to only return messages before this date
        sender_phone_number: Optional phone number to filter messages by sender
        chat_jid: Optional chat JID to filter messages by chat
        query: Optional search term to filter messages by content
        limit: Maximum number of messages to return (default 20)
        page: Page number for pagination (default 0)
        include_context: Whether to include messages before and after matches (default True)
        context_before: Number of messages to include before each match (default 1)
        context_after: Number of messages to include after each match (default 1)
    """
    messages = whatsapp_list_messages(
        after=after,
        before=before,
        sender_phone_number=sender_phone_number,
        chat_jid=chat_jid,
        query=query,
        limit=limit,
        page=page,
        include_context=include_context,
        context_before=context_before,
        context_after=context_after
    )
    return messages

@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Dict[str, Any]]:
    """Get WhatsApp chats matching specified criteria.
    
    Args:
        query: Optional search term to filter chats by name or JID
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
        include_last_message: Whether to include the last message in each chat (default True)
        sort_by: Field to sort results by, either "last_active" or "name" (default "last_active")
    """
    chats = whatsapp_list_chats(
        query=query,
        limit=limit,
        page=page,
        include_last_message=include_last_message,
        sort_by=sort_by
    )
    return chats

@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by JID.
    
    Args:
        chat_jid: The JID of the chat to retrieve
        include_last_message: Whether to include the last message (default True)
    """
    chat = whatsapp_get_chat(chat_jid, include_last_message)
    return chat

@mcp.tool()
def get_direct_chat_by_contact(sender_phone_number: str) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by sender phone number.
    
    Args:
        sender_phone_number: The phone number to search for
    """
    chat = whatsapp_get_direct_chat_by_contact(sender_phone_number)
    return chat

@mcp.tool()
def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Dict[str, Any]]:
    """Get all WhatsApp chats involving the contact.
    
    Args:
        jid: The contact's JID to search for
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
    """
    chats = whatsapp_get_contact_chats(jid, limit, page)
    return chats

@mcp.tool()
def get_last_interaction(jid: str) -> str:
    """Get most recent WhatsApp message involving the contact.
    
    Args:
        jid: The JID of the contact to search for
    """
    message = whatsapp_get_last_interaction(jid)
    return message

@mcp.tool()
def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> Dict[str, Any]:
    """Get context around a specific WhatsApp message.
    
    Args:
        message_id: The ID of the message to get context for
        before: Number of messages to include before the target message (default 5)
        after: Number of messages to include after the target message (default 5)
    """
    context = whatsapp_get_message_context(message_id, before, after)
    return context

@mcp.tool()
def send_message(
    recipient: str,
    message: str
) -> Dict[str, Any]:
    """Send a WhatsApp message to a person or group. For group chats use the JID.

    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        message: The message text to send
    
    Returns:
        A dictionary containing success status and a status message
    """
    # Validate input
    if not recipient:
        return {
            "success": False,
            "message": "Recipient must be provided"
        }
    
    # Call the whatsapp_send_message function with the unified recipient parameter
    success, status_message = whatsapp_send_message(recipient, message)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_file(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send a file such as a picture, raw audio, video or document via WhatsApp to the specified recipient. For group messages use the JID.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the media file to send (image, video, document)
    
    Returns:
        A dictionary containing success status and a status message
    """
    
    # Call the whatsapp_send_file function
    success, status_message = whatsapp_send_file(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_audio_message(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send any audio file as a WhatsApp audio message to the specified recipient. For group messages use the JID. If it errors due to ffmpeg not being installed, use send_file instead.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the audio file to send (will be converted to Opus .ogg if it's not a .ogg file)
    
    Returns:
        A dictionary containing success status and a status message
    """
    success, status_message = whatsapp_audio_voice_message(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def download_media(message_id: str, chat_jid: str) -> Dict[str, Any]:
    """Download media from a WhatsApp message and get the local file path.
    
    Args:
        message_id: The ID of the message containing the media
        chat_jid: The JID of the chat containing the message
    
    Returns:
        A dictionary containing success status, a status message, and the file path if successful
    """
    file_path = whatsapp_download_media(message_id, chat_jid)
    
    if file_path:
        return {
            "success": True,
            "message": "Media downloaded successfully",
            "file_path": file_path
        }
    else:
        return {
            "success": False,
            "message": "Failed to download media"
        }

def _resolve_chat_jid(group_name: str) -> Optional[str]:
    """Look up a chat JID by partial group name match."""
    chats = whatsapp_list_chats(query=group_name, limit=5, include_last_message=True)
    if not chats:
        return None
    if isinstance(chats[0], dict):
        return chats[0].get("jid")
    return getattr(chats[0], "jid", None)


@mcp.tool()
def extract_trip_itinerary(
    group_name: str,
    days_back: int = 30
) -> str:
    """Extract a structured trip itinerary from a WhatsApp group chat.

    Scans messages for dates, times, locations, bookings, and plans then
    returns a clean day-by-day itinerary. Great for girls trip planning groups.

    Args:
        group_name: Name or partial name of the WhatsApp group (e.g. "girls trip")
        days_back: How many days back to scan for messages (default: 30)
    """
    from datetime import datetime, timedelta

    chat_jid = _resolve_chat_jid(group_name)
    if not chat_jid:
        return f"Could not find a group matching '{group_name}'. Try list_chats to see available groups."

    after = (datetime.now() - timedelta(days=days_back)).isoformat()
    messages = whatsapp_list_messages(
        chat_jid=chat_jid,
        after=after,
        limit=500,
        include_context=False
    )

    if not messages or messages.startswith("No messages"):
        return "No messages found in this chat for the given time period."

    prompt_prefix = (
        "You are a helpful trip planner assistant. Below are WhatsApp messages from a group trip planning chat.\n"
        "Extract and organize all trip-related information into a clear, structured itinerary.\n"
        "Include: dates, times, locations, hotel/accommodation details, activities, restaurant bookings, "
        "transport plans, and any action items or things to confirm.\n"
        "If exact dates are missing, make a note. Format as a day-by-day plan where possible.\n\n"
        "MESSAGES:\n"
        f"{messages}\n\n"
        "ITINERARY:"
    )
    return prompt_prefix


@mcp.tool()
def extract_packing_list(
    group_name: str,
    days_back: int = 30
) -> str:
    """Extract a consolidated packing list from a WhatsApp group trip chat.

    Scans messages for things people said they'll bring, items mentioned as
    needed, and shared supplies. Returns a grouped packing list.

    Args:
        group_name: Name or partial name of the WhatsApp group (e.g. "girls trip")
        days_back: How many days back to scan for messages (default: 30)
    """
    from datetime import datetime, timedelta

    chat_jid = _resolve_chat_jid(group_name)
    if not chat_jid:
        return f"Could not find a group matching '{group_name}'. Try list_chats to see available groups."

    after = (datetime.now() - timedelta(days=days_back)).isoformat()
    messages = whatsapp_list_messages(
        chat_jid=chat_jid,
        after=after,
        limit=500,
        include_context=False
    )

    if not messages or messages.startswith("No messages"):
        return "No messages found in this chat for the given time period."

    prompt_prefix = (
        "You are a helpful trip assistant. Below are WhatsApp messages from a group trip planning chat.\n"
        "Extract and consolidate everything related to packing and what people are bringing.\n"
        "Look for: 'I'll bring', 'I'm packing', 'don't forget', 'we need', 'who's bringing', "
        "'reminder to pack', and similar phrases.\n"
        "Organize into categories: Clothes & Accessories, Toiletries, Tech & Gadgets, "
        "Food & Drinks, Shared Supplies, Documents & Money, and Other.\n"
        "For each item note who is bringing it if mentioned, and flag any items where no one "
        "has volunteered yet.\n\n"
        "MESSAGES:\n"
        f"{messages}\n\n"
        "PACKING LIST:"
    )
    return prompt_prefix


CHAT_LISTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_lists.json")


def _load_chat_lists() -> Dict[str, List[str]]:
    """Load chat list definitions from chat_lists.json."""
    if not os.path.exists(CHAT_LISTS_PATH):
        return {}
    with open(CHAT_LISTS_PATH, "r") as f:
        return json.load(f)


@mcp.tool()
def get_list_chats(list_name: str) -> str:
    """Get all WhatsApp chats and groups belonging to a custom list.

    Lists are defined in chat_lists.json — each list maps to a set of
    keywords matched against chat names. Similar to WhatsApp's built-in
    custom lists feature (Family, Work, Dance etc.).

    Args:
        list_name: Name of the list (e.g. "Dance", "Family", "Neighbors")
    """
    import sqlite3 as _sqlite3

    lists = _load_chat_lists()

    if not lists:
        return "No lists defined. Edit chat_lists.json in the whatsapp-mcp-server folder to create your lists."

    # Case-insensitive match for list name
    matched_key = next((k for k in lists if k.lower() == list_name.lower()), None)
    if not matched_key:
        available = ", ".join(lists.keys())
        return f"List '{list_name}' not found. Available lists: {available}"

    keywords = lists[matched_key]

    # Query ALL named chats directly from the database (no limit)
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'whatsapp-bridge', 'store', 'messages.db')
    try:
        conn = _sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.jid, c.name, c.last_message_time, m.content as last_message
            FROM chats c
            LEFT JOIN messages m ON c.jid = m.chat_jid AND c.last_message_time = m.timestamp
            WHERE c.name != ''
            ORDER BY c.last_message_time DESC
        """)
        all_chats = cursor.fetchall()
        conn.close()
    except _sqlite3.Error as e:
        return f"Database error: {e}"

    matches = [(jid, name, last_time, last_msg) for jid, name, last_time, last_msg in all_chats
               if any(kw.lower() in (name or '').lower() for kw in keywords)]

    if not matches:
        return f"No chats found for list '{matched_key}' with keywords: {keywords}\nTry editing chat_lists.json to adjust the keywords."

    lines = [f"📋 {matched_key} ({len(matches)} chats)\n"]
    for jid, name, last_time, last_msg in matches:
        preview = (last_msg[:60] + "...") if last_msg and len(last_msg) > 60 else (last_msg or "")
        lines.append(f"• {name}  [{last_time}]\n  {preview}")

    return "\n".join(lines)


@mcp.tool()
def show_all_lists() -> str:
    """Show all defined custom chat lists and their keyword filters.

    Returns your list names and the keywords used to match chats to each list.
    Edit chat_lists.json to add, remove or rename lists and keywords.
    """
    lists = _load_chat_lists()

    if not lists:
        return "No lists defined. Edit chat_lists.json in the whatsapp-mcp-server folder to create your lists."

    lines = ["📋 Your Custom Chat Lists\n"]
    for list_name, keywords in lists.items():
        lines.append(f"• {list_name}: {', '.join(keywords)}")
    lines.append(f"\nEdit: {CHAT_LISTS_PATH}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')