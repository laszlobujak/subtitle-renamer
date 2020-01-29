import os
import sys
import re
import shutil


class Episode(object):
    def __init__(self, file_name=None, folder=None, season=None, episode=None):
        self.file_name = file_name
        self.folder = folder
        self.season = season
        self.episode = episode

accepted_file_ext = [".avi", ".mkv", ".mp4", ".mp3", ".wmv"]
episodes_folder = sys.argv[1]
subtitles_folder = sys.argv[2]
id_matcher = ".?([0-9]+).?([0-9]+)"

def parse_data():
    parsed_episodes = []
    for path, _, episodes in os.walk(episodes_folder):
        for file in episodes:
            id = re.search(id_matcher, file, re.IGNORECASE)
            file_name, file_ext = os.path.splitext(file)
            if (id and ("sample" not in file) and (file_ext in accepted_file_ext)):
                video_season = id.group(1).zfill(2)
                video_episode = id.group(2).zfill(2)
                parsed_episodes.append(Episode(file_name, path, video_season, video_episode))
    return parsed_episodes

def process_subtitles(episodes):
    for path, _, subtitles in os.walk(subtitles_folder):
        for subtitle in subtitles:
            id = re.search(id_matcher, subtitle, re.IGNORECASE)
            if id:
                srt_season = id.group(1).zfill(2)
                srt_episode = id.group(2).zfill(2)
                for episode in episodes:
                    if episode.season == srt_season and episode.episode == srt_episode:
                        src = os.path.join(path, subtitle)
                        dst = os.path.join(episode.folder, episode.file_name + ".srt")
                        print("before: {}\nafter: {}\ncopied to: {}\n".format(subtitle, episode.file_name + ".srt", episode.folder))
                        shutil.copy(src, dst)
                        episodes.remove(episode)

episodes = parse_data()
process_subtitles(episodes)
