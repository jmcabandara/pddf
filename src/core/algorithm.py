import setting
from utils import LOG


class AbstractAlgorithm:
    def __init__(self):
        self.char_table = dict()
        self.files = list()

    def set_files(self, files):
        LOG.debug("%s set_files", self.__class__.__name__)
        self.files = files

    def find(self):
        raise Exception('find not implement')

    @property
    def dup_files(self):
        LOG.debug("%s dup_files", self.__class__.__name__)
        ret = list()
        for k, v in self.char_table.items():
#            LOG.debug("{0} {1}".format(k, v))
#            LOG.debug(k)
            if len(v) > 1:
                ret.append(v)
        return ret

    @property
    def filtered_files(self):
        LOG.debug("%s filtered_files", self.__class__.__name__)
        ret = list()
        for k, v in self.char_table.items():
            LOG.debug("{0} {1}".format(k, v))
            if len(v) > 1:
                ret.extend(v)
        return ret


class FullScanner(AbstractAlgorithm):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            md5sum = _file.md5sum
            if md5sum == setting.UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(md5sum)
            if entry:
                entry.append(_file)
            else:
                self.char_table[md5sum] = [_file]


class SizeChecker(AbstractAlgorithm):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            character = _file.size
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]


class CharacterScanner(AbstractAlgorithm):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        for _file in self.files:
            character = _file.character
            if character == setting.UNKNOWN_SYMBOL:
                continue
            entry = self.char_table.get(character)
            if entry:
                entry.append(_file)
            else:
                self.char_table[character] = [_file]


class HybridQuick(AbstractAlgorithm):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        LOG.debug("size_checker find start")
        size_checker = SizeChecker()
        size_checker.set_files(self.files)
        size_checker.find()
        LOG.debug("size_checker find finish")
        LOG.debug("character_scanner find start")
        character_scanner = CharacterScanner()
        character_scanner.set_files(size_checker.filtered_files)
        character_scanner.find()
        LOG.info("character_scanner find finish")
        self.char_table = character_scanner.char_table


class HybridFull(AbstractAlgorithm):
    def find(self):
        LOG.debug("%s find", self.__class__.__name__)
        size_checker = SizeChecker()
        size_checker.set_files(self.files)
        size_checker.find()
        character_scanner = CharacterScanner()
        character_scanner.set_files(size_checker.filtered_files)
        character_scanner.find()
        full_scanner = FullScanner()
        full_scanner.set_files(character_scanner.filtered_files)
        full_scanner.find()
        self.char_table = full_scanner.char_table
