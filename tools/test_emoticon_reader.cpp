// 验证正式资源能由共享引擎读取；不依赖任何平台 UI。
#include "bimkit/theme/emoticon_pack.h"
#include <cassert>
#include <filesystem>
#include <iostream>
#include <set>
int main(int argc, char** argv) {
    assert(argc == 2);
    const auto directory = (std::filesystem::path(argv[1]) / "emoticons").string();
    bimkit::EmoticonPackReader reader("", directory);
    const auto packs = reader.list();
    assert(packs.size() == 2 && packs[0].id == "default" && packs[1].id == "kaomoji");
    assert(packs[1].name == "颜文字");
    bimkit::EmoticonPack emoji, kaomoji;
    assert(reader.load("default", emoji) == bimkit::BimkitError::SUCCESS);
    assert(reader.load("kaomoji", kaomoji) == bimkit::BimkitError::SUCCESS);
    assert(emoji.groups.size() == 22 && emoji.groups[0].id == "common" && emoji.groups[0].items.size() == 64);
    size_t count = 0; std::set<std::string> values, ids;
    for (const auto& group : emoji.groups) for (const auto& item : group.items) {
        assert(item.kind == "text" && ids.insert(item.id).second);
        ++count; values.insert(item.text);
    }
    assert(count == 4036 && values.size() == 3972);
    assert(kaomoji.groups.size() == 32);
    size_t single = 0, multi = 0; values.clear(); ids.clear();
    for (const auto& group : kaomoji.groups) for (const auto& item : group.items) {
        assert(item.kind == "text" && values.insert(item.text).second && ids.insert(item.id).second);
        if (item.text.find('\n') == std::string::npos) ++single; else ++multi;
    }
    assert(single == 1074 && multi == 222);
    std::cout << "PASS: shared reader, 2 packs, Emoji 22 categories/3972 unique/64 shortcuts, kaomoji 32 categories/1296 strings\n";
}
